import punq

from src.infrastructure.repositories.couples.base import BaseCouplesRepository
from src.infrastructure.repositories.couples.memory import MemoryCouplesRepository
from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.infrastructure.repositories.users.memory import MemoryUsersRepository
from src.project.containers import _init_container


def init_dummy_container() -> punq.Container:
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
