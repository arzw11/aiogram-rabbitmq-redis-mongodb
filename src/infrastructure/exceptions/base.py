from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class InfrastructureException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Произошла инфраструктурная ошибка.'
