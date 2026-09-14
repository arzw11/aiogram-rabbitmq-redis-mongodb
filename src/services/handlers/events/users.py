from dataclasses import dataclass

from src.domain.events.users import UserCreatedEvent
from src.infrastructure.message_brokers.converters import convert_event_to_broker_message
from src.services.handlers.events.base import EventHandler


@dataclass
class UserCreatedEventHandler(EventHandler[UserCreatedEvent, None]):
    async def handle(self, event: UserCreatedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            key='events.users.created',
            value=convert_event_to_broker_message(event=event),
        )
