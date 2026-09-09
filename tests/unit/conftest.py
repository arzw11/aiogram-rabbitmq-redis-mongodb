import punq
import pytest

from src.infrastructure.repositories.couples.base import BaseCouplesRepository
from src.infrastructure.repositories.users.base import BaseUsersRepository
from tests.fixtures import init_unit_container


@pytest.fixture()
def unit_container() -> punq.Container:
    return init_unit_container()


@pytest.fixture()
def user_repo(unit_container: punq.Container) -> BaseUsersRepository:
    return unit_container.resolve(BaseUsersRepository)


@pytest.fixture()
def couple_repo(unit_container: punq.Container) -> BaseCouplesRepository:
    return unit_container.resolve(BaseCouplesRepository)
