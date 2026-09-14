import punq
import pytest

from src.infrastructure.message_brokers.base import BaseMessageBroker
from src.infrastructure.repositories.couples.base import BaseCouplesRepository
from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.services.mediator.base import Mediator
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


@pytest.fixture()
def unit_mediator(unit_container: punq.Container) -> Mediator:
    return unit_container.resolve(Mediator)


@pytest.fixture()
def unit_message_broker(unit_container: punq.Container) -> BaseMessageBroker:
    return unit_container.resolve(BaseMessageBroker)
