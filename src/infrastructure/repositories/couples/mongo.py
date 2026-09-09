from dataclasses import dataclass

from src.domain.entities.couples import Couple
from src.infrastructure.repositories.couples.base import BaseCouplesRepository
from src.infrastructure.repositories.couples.converters import (
    convert_couple_document_to_entity,
    convert_couple_entity_to_document,
)
from src.infrastructure.repositories.mongo import BaseMongoDBRepository


@dataclass
class MongoDBCouplesRepository(BaseCouplesRepository, BaseMongoDBRepository):
    async def create(self, couple: Couple) -> Couple:
        await self._collection.insert_one(
            document=convert_couple_entity_to_document(couple=couple),
        )

        return couple

    async def get_by_oid(self, oid: str) -> Couple | None:
        couple_document = await self._collection.find_one(filter={"oid": oid})

        if not couple_document:
            return None

        return convert_couple_document_to_entity(couple_document=couple_document)

    async def update_by_oid(self, oid: str, couple: Couple) -> bool:
        couple_document = convert_couple_entity_to_document(couple=couple)
        couple_document.pop("oid")

        result = await self._collection.update_one(
            filter={"oid": oid},
            update={"$set": couple_document},
        )

        return result.modified_count > 0
