import punq
import pytest

from src.infrastructure.repositories.couples.base import BaseCouplesRepository
from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.services.mediator.base import Mediator
from tests.fixtures import init_integration_container


@pytest.fixture()
def integration_container() -> punq.Container:
    return init_integration_container()


@pytest.fixture()
def mongo_user_repo(integration_container: punq.Container) -> BaseUsersRepository:
    return integration_container.resolve(BaseUsersRepository)


@pytest.fixture()
def mongo_couple_repo(integration_container: punq.Container) -> BaseCouplesRepository:
    return integration_container.resolve(BaseCouplesRepository)


@pytest.fixture()
def integration_mediator(integration_container: punq.Container) -> Mediator:
    return integration_container.resolve(Mediator)
