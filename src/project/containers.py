from functools import lru_cache

import punq

from src.infrastructure.repositories.couples.base import BaseCouplesRepository
from src.infrastructure.repositories.couples.memory import MemoryCouplesRepository
from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.infrastructure.repositories.users.memory import MemoryUsersRepository


@lru_cache(1)
def get_container() -> punq.Container:
    return _init_container()


def _init_container() -> punq.Container:
    container: punq.Container = punq.Container()

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
