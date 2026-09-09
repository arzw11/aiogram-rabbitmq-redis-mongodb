from dataclasses import dataclass

from src.domain.events.base import BaseEvent


@dataclass
class UserCreatedEvent(BaseEvent):
    event_title = "New user created."

    user_oid: str
    user_telegram_id: int
    user_name: str | None = None
