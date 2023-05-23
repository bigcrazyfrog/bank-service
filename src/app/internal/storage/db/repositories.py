from django.core.files.storage import Storage

from app.internal.storage.domain.service import IStorageRepository
from config.settings import AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME


class StorageRepository(IStorageRepository):
    def __init__(self, storage: Storage):
        self._storage = storage


    def create(self, content: bytearray) -> str:
        alternative_name = self._storage.get_alternative_name("postcard", ".jpg")
        file = self._storage.open(alternative_name, "w")
        file.write(content)
        file.close()

        return f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/{alternative_name}"
