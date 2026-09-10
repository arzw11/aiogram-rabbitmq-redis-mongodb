from functools import lru_cache

import punq
from motor.motor_asyncio import AsyncIOMotorClient

from src.domain.commands.couples import CreateCoupleCommand, FormCoupleCommand, GetCoupleByOIDCommand
from src.domain.commands.users import CreateUserCommand, GetUserByOIDCommand, GetUserByTelegramIDCommand
from src.infrastructure.repositories.couples.base import BaseCouplesRepository
from src.infrastructure.repositories.couples.mongo import MongoDBCouplesRepository
from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.infrastructure.repositories.users.mongo import MongoDBUsersRepository
from src.project.configs import settings
from src.services.handlers.commands.couples import (
    CreateCoupleCommandHandler,
    FormCoupleCommandHandler,
    GetCoupleByOIDCommandHandler,
)
from src.services.handlers.commands.users import (
    CreateUserCommandHandler,
    GetUserByOIDCommandHandler,
    GetUserByTelegramIDCommandHandler,
)
from src.services.mediator.base import Mediator


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

    # mediator
    def init_mediator() -> Mediator:
        mediator: Mediator = Mediator()

        # user command handlers
        mediator.register_command(
            command=CreateUserCommand,
            command_handlers=[
                CreateUserCommandHandler(
                    _event_mediator=mediator,
                    users_repository=container.resolve(BaseUsersRepository),
                ),
            ],
        )
        mediator.register_command(
            command=GetUserByOIDCommand,
            command_handlers=[
                GetUserByOIDCommandHandler(
                    _event_mediator=mediator,
                    users_repository=container.resolve(BaseUsersRepository),
                ),
            ],
        )
        mediator.register_command(
            command=GetUserByTelegramIDCommand,
            command_handlers=[
                GetUserByTelegramIDCommandHandler(
                    _event_mediator=mediator,
                    users_repository=container.resolve(BaseUsersRepository),
                ),
            ],
        )

        # couple command handlers
        mediator.register_command(
            command=CreateCoupleCommand,
            command_handlers=[
                CreateCoupleCommandHandler(
                    _event_mediator=mediator,
                    couples_repository=container.resolve(BaseCouplesRepository),
                ),
            ],
        )
        mediator.register_command(
            command=GetCoupleByOIDCommand,
            command_handlers=[
                GetCoupleByOIDCommandHandler(
                    _event_mediator=mediator,
                    couples_repository=container.resolve(BaseCouplesRepository),
                ),
            ],
        )
        mediator.register_command(
            command=FormCoupleCommand,
            command_handlers=[
                FormCoupleCommandHandler(
                    _event_mediator=mediator,
                    couples_repository=container.resolve(BaseCouplesRepository),
                ),
            ],
        )

        return mediator

    container.register(
        service=Mediator,
        factory=init_mediator,
        scope=punq.Scope.transient,
    )

    return container
