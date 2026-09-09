import pytest
from faker import Faker

from src.domain.entities.couples import Couple
from src.domain.entities.users import User
from src.domain.events.couples import (
    CoupleCreatedEvent,
    CoupleFormedEvent,
)
from src.domain.exceptions.couples import (
    CannotAddSameUserToCoupleError,
    CoupleAlreadyHasSecondUserException,
)
from tests.factories.couples import CoupleEntityFactory
from tests.factories.users import UserEntityFactory


def test_create_couple(faker: Faker):
    user: User = UserEntityFactory.create()
    couple: Couple = Couple.create_couple(
        title=faker.text(max_nb_chars=64),
        first_user_oid=user.oid,
    )

    assert isinstance(couple, Couple), f"{couple=}"
    assert couple.first_user_oid == user.oid, f"{couple=}"
    assert isinstance(couple._events[0], CoupleCreatedEvent), f"{couple=}"


def test_couple_add_second_user():
    user1, user2 = UserEntityFactory.create_batch(size=2)
    couple: Couple = CoupleEntityFactory.create(first_user_oid=user1.oid)

    assert isinstance(couple, Couple), f"{couple=}"
    assert couple.first_user_oid == user1.oid, f"{couple=}"

    couple.add_second_user(user2)

    assert isinstance(couple._events[0], CoupleFormedEvent), f"{couple=}"


def test_couple_add_same_user():
    user: User = UserEntityFactory.create()
    couple: Couple = CoupleEntityFactory.create(first_user_oid=user.oid)

    with pytest.raises(CannotAddSameUserToCoupleError):
        couple.add_second_user(second_user_oid=user.oid)


def test_couple_already_has_second_user():
    user1, user2 = UserEntityFactory.create_batch(size=2)
    couple: Couple = CoupleEntityFactory.create(first_user_oid=user1.oid)
    couple.add_second_user(user2.oid)

    with pytest.raises(CoupleAlreadyHasSecondUserException):
        couple.add_second_user(second_user_oid=user2.oid)
