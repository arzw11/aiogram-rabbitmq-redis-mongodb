from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class CoupleAlreadyHasSecondUserException(ApplicationException):
    couple_oid: str

    @property
    def message(self) -> str:
        return "Пара уже сформирована."


@dataclass(eq=False)
class CannotAddSameUserToCoupleException(ApplicationException):
    couple_oid: str
    first_user_oid: str
    second_user_oid: str

    @property
    def message(self) -> str:
        return "Пользователь не может формировать пару с самим собой."
