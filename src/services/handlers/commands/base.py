from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from src.domain.commands.base import BaseCommand
from src.services.mediator.event import EventMediator

CT = TypeVar('CT', bound=BaseCommand)
CR = TypeVar('CR', bound=Any)


@dataclass(frozen=True)
class CommandHandler(ABC, Generic[CT, CR]):
    _event_mediator: EventMediator

    @abstractmethod
    async def handle(self, command: CT) -> CR: ...
