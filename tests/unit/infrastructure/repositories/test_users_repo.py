import pytest
from faker import Faker
from tests.factories.users import UserEntityFactory

from src.domain.entities.users import User
from src.infrastructure.repositories.users.base import BaseUsersRepository


@pytest.mark.asyncio
async def test_user_repo_create(user_repo: BaseUsersRepository):
    user: User = UserEntityFactory.create()
    created_user: User = await user_repo.create(user=user)

    assert created_user == user, f"{created_user=}"


@pytest.mark.asyncio
async def test_user_repo_create_batch(faker: Faker, user_repo: BaseUsersRepository):
    size: int = faker.pyint(min_value=1, max_value=10)
    users: list[User] = UserEntityFactory.create_batch(size=size)

    created_users: list[User] = [await user_repo.create(user) for user in users]

    assert len(created_users) == size, f"{created_users=}"


@pytest.mark.asyncio
async def test_user_repo_get_by_oid(user_repo: BaseUsersRepository):
    user: User = UserEntityFactory.create()
    await user_repo.create(user=user)

    fetched_user: User = await user_repo.get_by_oid(oid=user.oid)

    assert fetched_user == user, f"{fetched_user=}"


@pytest.mark.asyncio
async def test_user_repo_get_by_oid_none(faker: Faker, user_repo: BaseUsersRepository):
    fetched_user: None = await user_repo.get_by_oid(oid=faker.text(max_nb_chars=32))

    assert not fetched_user, f"{fetched_user=}"


@pytest.mark.asyncio
async def test_user_repo_get_by_telegram_id(user_repo: BaseUsersRepository):
    user: User = UserEntityFactory.create()
    await user_repo.create(user=user)

    fetched_user: User = await user_repo.get_by_telegram_id(telegram_id=user.telegram_id)

    assert fetched_user == user, f"{fetched_user=}"


@pytest.mark.asyncio
async def test_user_repo_get_by_telegram_id_none(faker: Faker, user_repo: BaseUsersRepository):
    fetched_user: None = await user_repo.get_by_telegram_id(telegram_id=faker.pyint())

    assert not fetched_user, f"{fetched_user=}"
