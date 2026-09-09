import punq
from mongomock_motor import AsyncMongoMockClient
from motor.motor_asyncio import AsyncIOMotorClient

from src.infrastructure.repositories.couples.base import BaseCouplesRepository
from src.infrastructure.repositories.couples.memory import MemoryCouplesRepository
from src.infrastructure.repositories.couples.mongo import MongoDBCouplesRepository
from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.infrastructure.repositories.users.memory import MemoryUsersRepository
from src.infrastructure.repositories.users.mongo import MongoDBUsersRepository
from src.project.configs import settings
from src.project.containers import _init_container


def init_unit_container() -> punq.Container:
    container: punq.Container = _init_container()

    # repositories
    container.register(
        service=BaseUsersRepository,
        factory=MemoryUsersRepository,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=BaseCouplesRepository,
        factory=MemoryCouplesRepository,
        scope=punq.Scope.singleton,
    )

    return container


def init_integration_container() -> punq.Container:
    container: punq.Container = _init_container()

    def create_mock_mongdb_client() -> AsyncIOMotorClient:
        return AsyncMongoMockClient()

    container.register(
        service=AsyncIOMotorClient,
        factory=create_mock_mongdb_client,
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
            collection_title=settings.MONGODB_USERS_COLLECTION,
        ),
        scope=punq.Scope.singleton,
    )

    return container
