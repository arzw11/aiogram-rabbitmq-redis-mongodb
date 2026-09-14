from dataclasses import dataclass

from src.infrastructure.exceptions.base import InfrastructureException


@dataclass(eq=False)
class ChannelNotInitedException(InfrastructureException):
    @property
    def message(self) -> str:
        return "Канал не инициализирован."
