from dataclasses import (
    dataclass,
    field,
)

from src.domain.entities.base import BaseEntity
from src.domain.events.couples import (
    CoupleCreatedEvent,
    CoupleFormedEvent,
)
from src.domain.exceptions.couples import (
    CannotAddSameUserToCoupleError,
    CoupleAlreadyHasSecondUserException,
)


@dataclass(eq=False)
class Couple(BaseEntity):
    title: str
    first_user_oid: str
    second_user_oid: str | None = field(
        default=None,
        kw_only=True,
    )

    @classmethod
    def create_couple(cls, title: str, first_user_oid: str) -> "Couple":
        created_couple = cls(title=title, first_user_oid=first_user_oid)
        created_couple.register_event(
            event=CoupleCreatedEvent(
                couple_oid=created_couple.oid,
                couple_title=created_couple.title,
                first_user_oid=created_couple.first_user_oid,
            ),
        )

        return created_couple

    def add_second_user(self, second_user_oid: str) -> None:
        if self.second_user_oid is not None:
            raise CoupleAlreadyHasSecondUserException(self.oid)

        if self.first_user_oid == second_user_oid:
            raise CannotAddSameUserToCoupleError(
                couple_oid=self.oid,
                first_user_oid=self.first_user_oid,
                second_user_oid=second_user_oid,
            )

        self.second_user_oid = second_user_oid
        self.register_event(
            event=CoupleFormedEvent(
                couple_oid=self.oid,
                couple_title=self.title,
                first_user_oid=self.first_user_oid,
                second_user_oid=self.second_user_oid,
            ),
        )
