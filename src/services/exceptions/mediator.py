from dataclasses import dataclass

from src.services.exceptions.base import ServiceException


@dataclass(eq=False)
class EventHandlersNotRegisteredException(ServiceException):
    event_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики для события: {self.event_type}"


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(ServiceException):
    command_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики для команды: {self.command_type}"
