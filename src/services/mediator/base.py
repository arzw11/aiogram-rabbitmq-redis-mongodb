from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from src.domain.commands.base import BaseCommand
from src.domain.events.base import BaseEvent
from src.services.exceptions.mediator import CommandHandlersNotRegisteredException, EventHandlersNotRegisteredException
from src.services.handlers.commands.base import CR, CT, CommandHandler
from src.services.handlers.events.base import ER, ET, EventHandler
from src.services.mediator.command import CommandMediator
from src.services.mediator.event import EventMediator


@dataclass(eq=False)
class Mediator(CommandMediator, EventMediator):
    commands_map: dict[CT, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    events_map: dict[ET, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]):
        self.events_map[event].extend(event_handlers)

    def register_command(self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]):
        self.commands_map[command].extend(command_handlers)

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        result = []

        for event in events:
            handlers: Iterable[EventHandler] = self.events_map[event.__class__]

            if not handlers:
                raise EventHandlersNotRegisteredException(event_type=event.__class__)

            result.extend([await handler.handle(event) for handler in handlers])

        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type=command_type)

        return [await handler.handle(command) for handler in handlers]
