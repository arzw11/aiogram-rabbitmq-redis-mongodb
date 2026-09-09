import punq
import pytest

from src.infrastructure.repositories.users.base import BaseUsersRepository
from tests.fixtures import init_dummy_container


@pytest.fixture()
def container() -> punq.Container:
    return init_dummy_container()


@pytest.fixture()
def user_repo(container: punq.Container) -> BaseUsersRepository:
    return container.resolve(BaseUsersRepository)
