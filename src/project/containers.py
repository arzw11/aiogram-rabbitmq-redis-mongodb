from functools import lru_cache

import punq
from motor.motor_asyncio import AsyncIOMotorClient

from src.infrastructure.repositories.couples.base import BaseCouplesRepository
from src.infrastructure.repositories.couples.mongo import MongoDBCouplesRepository
from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.infrastructure.repositories.users.mongo import MongoDBUsersRepository
from src.project.configs import settings


@lru_cache(1)
def get_container() -> punq.Container:
    return _init_container()


def _init_container() -> punq.Container:
    container: punq.Container = punq.Container()

    # mongodb
    def create_mongodb_client() -> AsyncIOMotorClient:
        return AsyncIOMotorClient(settings.MONGO_DB_CONNECTION_URI, serverSelectionTimeoutMS=3000)

    container.register(
        service=AsyncIOMotorClient,
        factory=create_mongodb_client,
        scope=punq.Scope.singleton,
    )

    # repositories
    container.register(
        service=BaseUsersRepository,
        factory=lambda: MongoDBUsersRepository(
            mongo_db_client=container.resolve(AsyncIOMotorClient),
            database_title=settings.MONGODB_USERS_DATABASE,
            collection_title=settings.MONGODB_USERS_COLLECTION,
        ),
        scope=punq.Scope.singleton,
    )
    container.register(
        service=BaseCouplesRepository,
        factory=lambda: MongoDBCouplesRepository(
            mongo_db_client=container.resolve(AsyncIOMotorClient),
            database_title=settings.MONGODB_COUPLES_DATABASE,
            collection_title=settings.MONGODB_COUPLES_COLLECTION,
        ),
        scope=punq.Scope.singleton,
    )

    return container
