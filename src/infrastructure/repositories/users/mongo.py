from dataclasses import dataclass

from src.domain.entities.users import User
from src.infrastructure.repositories.mongo import BaseMongoDBRepository
from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.infrastructure.repositories.users.converters import (
    convert_user_document_to_entity,
    convert_user_entity_to_document,
)


@dataclass
class MongoDBUsersRepository(BaseUsersRepository, BaseMongoDBRepository):
    async def create(self, user: User) -> User:
        await self._collection.insert_one(
            document=convert_user_entity_to_document(user=user),
        )

        return user

    async def get_by_oid(self, oid: str) -> User | None:
        user_document = await self._collection.find_one(filter={"oid": oid})

        if not user_document:
            return None

        return convert_user_document_to_entity(user_document=user_document)

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        user_document = await self._collection.find_one(filter={"telegram_id": telegram_id})

        if not user_document:
            return None

        return convert_user_document_to_entity(user_document=user_document)
