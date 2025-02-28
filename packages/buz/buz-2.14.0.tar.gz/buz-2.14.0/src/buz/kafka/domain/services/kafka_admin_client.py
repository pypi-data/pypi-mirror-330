from __future__ import annotations

from abc import abstractmethod, ABC
from datetime import datetime
from typing import Sequence

from buz.kafka.domain.models.create_kafka_topic import CreateKafkaTopic
from buz.kafka.infrastructure.interfaces.connection_manager import ConnectionManager

DEFAULT_NUMBER_OF_MESSAGES_TO_POLLING = 999


class KafkaAdminClient(ConnectionManager, ABC):
    @abstractmethod
    def create_topics(
        self,
        *,
        topics: Sequence[CreateKafkaTopic],
    ) -> None:
        pass

    @abstractmethod
    def is_topic_created(
        self,
        topic: str,
    ) -> bool:
        pass

    @abstractmethod
    def delete_topics(
        self,
        *,
        topics: set[str],
    ) -> None:
        pass

    @abstractmethod
    def get_topics(
        self,
    ) -> set[str]:
        pass

    # This function moves the following offset from the provided date
    # if there are no messages with a date greater than the provided offset
    # the offset will be moved to the end
    @abstractmethod
    def move_offsets_to_datetime(
        self,
        *,
        consumer_group: str,
        topic: str,
        target_datetime: datetime,
    ) -> None:
        pass
