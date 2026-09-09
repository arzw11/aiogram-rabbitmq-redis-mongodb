from dataclasses import dataclass, field

from src.domain.entities.users import User
from src.infrastructure.repositories.users.base import BaseUsersRepository


@dataclass
class MemoryUsersRepository(BaseUsersRepository):
    _users: list[User] = field(
        default_factory=list,
        kw_only=True,
    )

    async def create(self, user: User) -> User:
        self._users.append(user)
        return user

    async def get_by_oid(self, oid: str) -> User | None:
        try:
            return next(user for user in self._users if user.oid == oid)
        except StopIteration:
            return None

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        try:
            return next(user for user in self._users if user.telegram_id == telegram_id)
        except StopIteration:
            return None
