from dataclasses import (
    dataclass,
    field,
)

from src.domain.entities.base import BaseEntity
from src.domain.events.users import UserCreatedEvent


@dataclass
class User(BaseEntity):
    telegram_id: int | None = field(
        default=None,
        kw_only=True,
    )
    name: str | None = field(
        default=None,
        kw_only=True,
    )

    @classmethod
    def create_user(
        cls,
        telegram_id: int | None = None,
        name: str | None = None,
    ) -> "User":
        created_user = cls(telegram_id=telegram_id, name=name)
        created_user.register_event(
            UserCreatedEvent(
                user_oid=created_user.oid,
                user_telegram_id=created_user.telegram_id,
                user_name=created_user.name,
            ),
        )
        return created_user
