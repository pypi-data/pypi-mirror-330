from __future__ import annotations


class NotAllPartitionAssignedException(Exception):
    def __init__(self, topic_name: str) -> None:
        super().__init__(
            f'Not all the partition were assigned for the topic "{topic_name}", please disconnect the rest of subscribers'
        )
