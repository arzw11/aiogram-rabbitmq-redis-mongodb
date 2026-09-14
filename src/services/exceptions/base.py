from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class ServiceException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Произошла сервисная ошибка.'
