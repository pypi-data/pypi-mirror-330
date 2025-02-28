from __future__ import annotations

from datetime import datetime
from logging import Logger
import re
from typing import Any, Callable, Optional, Sequence, cast

from cachetools import TTLCache
from kafka import KafkaClient, KafkaConsumer
from kafka.admin import KafkaAdminClient as KafkaPythonLibraryAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from kafka.structs import TopicPartition, OffsetAndTimestamp

from buz.kafka.domain.exceptions.not_all_partition_assigned_exception import NotAllPartitionAssignedException
from buz.kafka.domain.exceptions.topic_already_created_exception import KafkaTopicsAlreadyCreatedException
from buz.kafka.domain.exceptions.topic_not_found_exception import TopicNotFoundException
from buz.kafka.domain.models.consumer_initial_offset_position import ConsumerInitialOffsetPosition
from buz.kafka.domain.models.create_kafka_topic import CreateKafkaTopic
from buz.kafka.domain.models.kafka_connection_config import KafkaConnectionConfig
from buz.kafka.domain.services.kafka_admin_client import KafkaAdminClient

from buz.kafka.infrastructure.kafka_python.translators.consumer_initial_offset_position_translator import (
    KafkaPythonConsumerInitialOffsetPositionTranslator,
)

INTERNAL_KAFKA_TOPICS = {"__consumer_offsets", "_schema"}
TOPIC_CACHE_KEY = "topics"


class KafkaPythonAdminClient(KafkaAdminClient):
    __PYTHON_KAFKA_DUPLICATED_TOPIC_ERROR_CODE = 36

    _kafka_admin: Optional[KafkaPythonLibraryAdminClient] = None
    _kafka_client: Optional[KafkaClient] = None

    def __init__(
        self,
        *,
        logger: Logger,
        connection_config: KafkaConnectionConfig,
        cache_ttl_seconds: int = 0,
    ):
        self._logger = logger
        self.__connection_config = connection_config
        self._config_in_library_format = self.__get_kafka_config_in_library_format(self.__connection_config)
        self.__ttl_cache: TTLCache[str, Any] = TTLCache(maxsize=1, ttl=cache_ttl_seconds)

    def __get_kafka_config_in_library_format(self, config: KafkaConnectionConfig) -> dict:
        return {
            "client_id": config.client_id,
            "bootstrap_servers": config.bootstrap_servers,
            "security_protocol": config.credentials.security_protocol.value,
            "sasl_mechanism": config.credentials.sasl_mechanism.value if config.credentials.sasl_mechanism else None,
            "sasl_plain_username": config.credentials.user,
            "sasl_plain_password": config.credentials.password,
        }

    def connect(self):
        self._get_kafka_admin()
        self._get_kafka_client()

    def disconnect(self):
        if self._kafka_admin is not None:
            self._kafka_admin.close()
            self._kafka_admin = None
        if self._kafka_client is not None:
            self._kafka_client.close()
            self._kafka_client = None

    def _get_kafka_admin(self) -> KafkaPythonLibraryAdminClient:
        if not self._kafka_admin:
            self._kafka_admin = KafkaPythonLibraryAdminClient(**self._config_in_library_format)
        return self._kafka_admin

    def _get_kafka_client(self) -> KafkaClient:
        if not self._kafka_client:
            self._kafka_client = KafkaClient(**self._config_in_library_format)
        return self._kafka_client

    def create_topics(
        self,
        *,
        topics: Sequence[CreateKafkaTopic],
    ) -> None:
        new_topics = [
            NewTopic(
                name=topic.name,
                num_partitions=topic.partitions,
                replication_factor=topic.replication_factor,
                topic_configs=topic.configs,
            )
            for topic in topics
        ]

        try:
            self._get_kafka_admin().create_topics(new_topics=new_topics)
        except TopicAlreadyExistsError as error:
            topic_names = self.__get_list_of_kafka_topics_from_topic_already_exists_error(error)
            raise KafkaTopicsAlreadyCreatedException(topic_names=topic_names)

    def __get_list_of_kafka_topics_from_topic_already_exists_error(self, error: TopicAlreadyExistsError) -> list[str]:
        message = str(error)
        response_message = re.search(r"topic_errors=\[.*?]", message)
        topic_messages = re.findall(
            r"topic='[^']*', error_code=" + str(self.__PYTHON_KAFKA_DUPLICATED_TOPIC_ERROR_CODE), response_message[0]  # type: ignore
        )

        return [re.search("'.*'", topic_message)[0].strip("'") for topic_message in topic_messages]  # type: ignore

    def is_topic_created(
        self,
        topic: str,
    ) -> bool:
        return topic in self.get_topics()

    def get_topics(
        self,
    ) -> set[str]:
        return self.__resolve_cached_property(
            TOPIC_CACHE_KEY, lambda: set(self._get_kafka_admin().list_topics()) - INTERNAL_KAFKA_TOPICS
        )

    def __resolve_cached_property(self, property_key: str, callback: Callable) -> Any:
        value = self.__ttl_cache.get(property_key)
        if value is not None:
            return value
        value = callback()
        self.__ttl_cache[property_key] = value
        return value

    def delete_topics(
        self,
        *,
        topics: set[str],
    ) -> None:
        self._get_kafka_admin().delete_topics(
            topics=topics,
        )
        self.__remove_cache_property(TOPIC_CACHE_KEY)

    def __remove_cache_property(self, property_key: str) -> None:
        self.__ttl_cache.pop(property_key, None)

    def delete_subscription_groups(
        self,
        *,
        subscription_groups: set[str],
    ) -> None:
        self._get_kafka_admin().delete_consumer_groups(
            group_ids=subscription_groups,
        )

    def get_subscription_groups(
        self,
    ) -> set[str]:
        return set(self._get_kafka_admin().list_consumer_groups())

    def _wait_for_cluster_update(self) -> None:
        future = self._get_kafka_client().cluster.request_update()
        self._get_kafka_client().poll(future=future)

    def move_offsets_to_datetime(
        self,
        *,
        consumer_group: str,
        topic: str,
        target_datetime: datetime,
    ) -> None:
        consumer = KafkaConsumer(
            group_id=consumer_group,
            enable_auto_commit=False,
            auto_offset_reset=KafkaPythonConsumerInitialOffsetPositionTranslator.to_kafka_supported_format(
                ConsumerInitialOffsetPosition.BEGINNING
            ),
            **self._config_in_library_format,
        )

        partitions = consumer.partitions_for_topic(topic)

        if partitions is None:
            raise TopicNotFoundException(topic)

        topic_partitions = [TopicPartition(topic, p) for p in partitions]
        consumer.subscribe(topics=[topic])

        self.__force_partition_assignment(consumer)

        # We need all the partitions in order to update the offsets
        if len(consumer.assignment()) != len(topic_partitions):
            raise NotAllPartitionAssignedException(topic)

        offsets_for_date = self.__get_first_offset_after_date(
            consumer=consumer,
            topic_partitions=topic_partitions,
            target_datetime=target_datetime,
        )

        end_offsets = consumer.end_offsets(topic_partitions)

        if end_offsets is None or len(end_offsets.keys()) != len(topic_partitions):
            raise Exception(f'There was an error extracting the end offsets of the topic "{topic}"')

        for topic_partition in topic_partitions:
            offset_and_timestamp = offsets_for_date.get(topic_partition)
            if offset_and_timestamp:
                self._logger.info(f'moving "{topic_partition}" to the offset "{offset_and_timestamp.offset}"')
                consumer.seek(topic_partition, offset_and_timestamp.offset)
            else:
                self._logger.info(
                    f'moving "{topic_partition}" to the end of the topic because there are no messages later than "{target_datetime}"'
                )
                consumer.seek(topic_partition, end_offsets[topic_partition])

        consumer.commit()
        consumer.close()

    def __get_first_offset_after_date(
        self,
        *,
        consumer: KafkaConsumer,
        topic_partitions: Sequence[TopicPartition],
        target_datetime: datetime,
    ) -> dict[TopicPartition, Optional[OffsetAndTimestamp]]:
        offset_for_times: dict[TopicPartition, Optional[int]] = {}
        timestamp_ms = int(target_datetime.timestamp() * 1000)

        for topic_partition in topic_partitions:
            offset_for_times[topic_partition] = timestamp_ms

        return cast(
            dict[TopicPartition, Optional[OffsetAndTimestamp]],
            consumer.offsets_for_times(offset_for_times),
        )

    # We are not to commit the new offset, but we need to execute a polling in order to start the partition assignment
    def __force_partition_assignment(self, consumer: KafkaConsumer) -> None:
        consumer.poll(max_records=1, timeout_ms=0)
