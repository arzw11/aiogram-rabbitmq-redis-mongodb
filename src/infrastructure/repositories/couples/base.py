from abc import ABC, abstractmethod

from src.domain.entities.couples import Couple


class BaseCouplesRepository(ABC):
    @abstractmethod
    async def create(self, couple: Couple) -> Couple: ...

    @abstractmethod
    async def get_by_oid(self, oid: str) -> Couple | None: ...

    @abstractmethod
    async def update_by_oid(self, oid: str, couple: Couple) -> bool: ...
