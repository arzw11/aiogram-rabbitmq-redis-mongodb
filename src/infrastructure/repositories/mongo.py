from abc import ABC
from dataclasses import dataclass

from motor.core import AgnosticClient, AgnosticCollection


@dataclass
class BaseMongoDBRepository(ABC):
    mongodb_client: AgnosticClient
    database_title: str
    collection_title: str

    @property
    def _collection(self) -> AgnosticCollection:
        return self.mongodb_client[self.database_title][self.collection_title]
