from abc import ABC
from dataclasses import dataclass

from motor.core import AgnosticClient, AgnosticCollection


@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    database_title: str
    collection_title: str

    @property
    def _collection(self) -> AgnosticCollection:
        return self.mongo_db_client[self.database_title][self.collection_title]
