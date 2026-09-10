import pytest
from faker import Faker

from src.domain.commands.users import CreateUserCommand, GetUserByOIDCommand, GetUserByTelegramIDCommand
from src.domain.entities.users import User
from src.domain.events.users import UserCreatedEvent
from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.services.mediator.base import Mediator
from tests.factories.users import UserEntityFactory


@pytest.mark.asyncio
async def test_integration_create_user_command_handler(
    faker: Faker,
    integration_mediator: Mediator,
):
    telegram_id = faker.pyint()
    name = faker.name()
    command: CreateUserCommand = CreateUserCommand(
        telegram_id=telegram_id,
        name=name,
    )
    created_user, *_ = await integration_mediator.handle_command(command=command)

    assert isinstance(created_user, User), f"{created_user=}"
    assert created_user.telegram_id == telegram_id, f"{created_user=}"
    assert created_user.name == name, f"{created_user=}"
    assert len(created_user._events) > 0, f"{created_user=}"
    assert isinstance(created_user._events[0], UserCreatedEvent), f"{created_user=}"


@pytest.mark.asyncio
async def test_integration_get_user_by_oid_command_handler(
    mongo_user_repo: BaseUsersRepository,
    integration_mediator: Mediator,
):
    user: User = UserEntityFactory.create()
    created_user: User = await mongo_user_repo.create(user=user)
    command: GetUserByOIDCommand = GetUserByOIDCommand(oid=user.oid)

    fetched_user, *_ = await integration_mediator.handle_command(command=command)

    assert fetched_user == created_user, f"{fetched_user=}"
    assert fetched_user.telegram_id == created_user.telegram_id, f"{fetched_user=}"
    assert fetched_user.name == created_user.name, f"{fetched_user=}"


@pytest.mark.asyncio
async def test_integration_get_user_by_oid_command_handler_none(faker: Faker, integration_mediator: Mediator):
    fetched_user, *_ = await integration_mediator.handle_command(command=GetUserByOIDCommand(oid=faker.pystr()))

    assert fetched_user is None, f"{fetched_user}"


@pytest.mark.asyncio
async def test_integration_get_user_by_telegram_id_handler(
    mongo_user_repo: BaseUsersRepository,
    integration_mediator: Mediator,
):
    user: User = UserEntityFactory.create()
    created_user: User = await mongo_user_repo.create(user=user)
    command: GetUserByTelegramIDCommand = GetUserByTelegramIDCommand(telegram_id=created_user.telegram_id)

    fetched_user, *_ = await integration_mediator.handle_command(command=command)

    assert fetched_user == created_user, f"{fetched_user=}"
    assert fetched_user.telegram_id == created_user.telegram_id, f"{fetched_user=}"
    assert fetched_user.name == created_user.name, f"{fetched_user=}"


@pytest.mark.asyncio
async def test_integration_get_user_by_telegram_id_handler_none(faker: Faker, integration_mediator: Mediator):
    fetched_user, *_ = await integration_mediator.handle_command(
        command=GetUserByTelegramIDCommand(telegram_id=faker.pyint())
    )

    assert fetched_user is None, f"{fetched_user}"
