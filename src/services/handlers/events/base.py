from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from src.domain.events.base import BaseEvent
from src.infrastructure.message_brokers.base import BaseMessageBroker

ET = TypeVar('ET', bound=BaseEvent)
ER = TypeVar('ER', bound=Any)


@dataclass
class EventHandler(ABC, Generic[ET, ER]):
    message_broker: BaseMessageBroker
    broker_topic: str | None = field(default=None, kw_only=True)

    @abstractmethod
    async def handle(self, event: ET) -> ER: ...
