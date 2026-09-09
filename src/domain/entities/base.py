from abc import ABC
from copy import copy
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from uuid import uuid4

from src.domain.events.base import BaseEvent


@dataclass
class BaseEntity(ABC):
    oid: str = field(
        kw_only=True,
        default_factory=lambda: str(uuid4()),
    )
    _events: list[BaseEvent] = field(
        kw_only=True,
        default_factory=list,
    )
    created_at: datetime = field(
        kw_only=True,
        default_factory=datetime.now,
    )

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: "BaseEntity") -> bool:
        return self.oid == __value.oid

    def register_event(self, event: BaseEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[BaseEvent]:
        registered_events = copy(self._events)
        self._events.clear()

        return registered_events
