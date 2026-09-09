from dataclasses import dataclass

from src.domain.events.base import BaseEvent


@dataclass
class CoupleCreatedEvent(BaseEvent):
    event_title = "Couple created event."

    couple_oid: str
    couple_title: str
    first_user_oid: str


@dataclass
class CoupleFormedEvent(BaseEvent):
    event_title = "Couple formed event."

    couple_oid: str
    couple_title: str
    first_user_oid: str
    second_user_oid: str
