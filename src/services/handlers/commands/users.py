from dataclasses import dataclass

from src.domain.commands.users import CreateUserCommand, GetUserByOIDCommand, GetUserByTelegramIDCommand
from src.domain.entities.users import User
from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.services.handlers.commands.base import CommandHandler


@dataclass(frozen=True)
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, User]):
    users_repository: BaseUsersRepository

    async def handle(self, command: CreateUserCommand) -> User:
        user: User = User.create_user(
            telegram_id=command.telegram_id,
            name=command.name,
        )
        created_user: User = await self.users_repository.create(user=user)
        await self._event_mediator.publish(events=created_user.pull_events())

        return created_user


@dataclass(frozen=True)
class GetUserByOIDCommandHandler(CommandHandler[GetUserByOIDCommand, User | None]):
    users_repository: BaseUsersRepository

    async def handle(self, command: GetUserByOIDCommand) -> User | None:
        return await self.users_repository.get_by_oid(oid=command.user_oid)


@dataclass(frozen=True)
class GetUserByTelegramIDCommandHandler(CommandHandler[GetUserByTelegramIDCommand, User | None]):
    users_repository: BaseUsersRepository

    async def handle(self, command: GetUserByTelegramIDCommand) -> User | None:
        return await self.users_repository.get_by_telegram_id(telegram_id=command.telegram_id)
