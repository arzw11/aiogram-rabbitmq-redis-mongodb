from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.entities.users import User


@dataclass
class BaseUsersRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def get_by_oid(self, oid: str) -> User | None: ...

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> User | None: ...
