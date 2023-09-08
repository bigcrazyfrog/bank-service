from abc import ABC, abstractmethod


class IStorageRepository(ABC):
    """Interface for AWS S3 storage."""

    @abstractmethod
    def create(self, content: bytearray) -> str:
        ...
