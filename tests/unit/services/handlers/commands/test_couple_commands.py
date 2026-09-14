import pytest
from faker import Faker

from src.domain.commands.couples import CreateCoupleCommand, FormCoupleCommand, GetCoupleByOIDCommand
from src.domain.entities.couples import Couple
from src.domain.events.couples import CoupleCreatedEvent, CoupleFormedEvent
from src.domain.exceptions.couples import CannotAddSameUserToCoupleException, CoupleAlreadyHasSecondUserException
from src.infrastructure.repositories.couples.base import BaseCouplesRepository
from src.services.mediator.base import Mediator
from tests.factories.couples import CoupleEntityFactory


@pytest.mark.asyncio
async def test_create_couple_command_handler(faker: Faker, unit_mediator: Mediator):
    title = faker.text(max_nb_chars=64)
    first_user_oid = faker.pystr()
    command: CreateCoupleCommand = CreateCoupleCommand(title=title, first_user_oid=first_user_oid)
    created_couple, *_ = await unit_mediator.handle_command(command=command)

    assert isinstance(created_couple, Couple), f'{created_couple=}'
    assert created_couple.title == title, f'{created_couple=}'
    assert created_couple.first_user_oid == first_user_oid, f'{created_couple=}'
    assert len(created_couple._events) > 0, f'{created_couple=}'
    assert isinstance(created_couple._events[0], CoupleCreatedEvent), f'{created_couple=}'


@pytest.mark.asyncio
async def test_get_couple_by_oid_command_handler(
    couple_repo: BaseCouplesRepository,
    unit_mediator: Mediator,
):
    couple: Couple = CoupleEntityFactory.create()
    created_couple: Couple = await couple_repo.create(couple=couple)
    command: GetCoupleByOIDCommand = GetCoupleByOIDCommand(couple_oid=created_couple.oid)

    fetched_couple, *_ = await unit_mediator.handle_command(command=command)

    assert fetched_couple == created_couple, f'{created_couple=}'
    assert fetched_couple.title == created_couple.title, f'{fetched_couple=}'
    assert fetched_couple.first_user_oid == created_couple.first_user_oid, f'{fetched_couple=}'


@pytest.mark.asyncio
async def test_get_couple_by_oid_command_handler_none(faker: Faker, unit_mediator: Mediator):
    fetched_couple, *_ = await unit_mediator.handle_command(command=GetCoupleByOIDCommand(couple_oid=faker.pystr()))

    assert fetched_couple is None, f'{fetched_couple=}'


@pytest.mark.asyncio
async def test_form_couple_command_handler(
    faker: Faker,
    couple_repo: BaseCouplesRepository,
    unit_mediator: Mediator,
):
    second_user_oid: str = faker.pystr()
    couple: Couple = CoupleEntityFactory.create()
    created_couple: Couple = await couple_repo.create(couple=couple)
    command: FormCoupleCommand = FormCoupleCommand(
        couple_oid=created_couple.oid,
        second_user_oid=second_user_oid,
    )

    result, *_ = await unit_mediator.handle_command(command=command)

    assert result is True, f'{result=}'
    assert len(created_couple._events) > 0, f'{created_couple=}'
    assert isinstance(created_couple._events[0], CoupleFormedEvent), f'{created_couple=}'


@pytest.mark.asyncio
async def test_form_couple_command_handler_none(faker: Faker, unit_mediator: Mediator):
    command: FormCoupleCommand = FormCoupleCommand(
        couple_oid=faker.pystr(),
        second_user_oid=faker.pystr(),
    )
    result, *_ = await unit_mediator.handle_command(command=command)

    assert result is False, f'{result=}'


@pytest.mark.asyncio
async def test_form_couple_command_handler_already_has_second_user(
    faker: Faker,
    couple_repo: BaseCouplesRepository,
    unit_mediator: Mediator,
):
    second_user_oid: str = faker.pystr()
    couple: Couple = CoupleEntityFactory.create()
    couple.second_user_oid = second_user_oid
    created_couple: Couple = await couple_repo.create(couple=couple)
    command: FormCoupleCommand = FormCoupleCommand(
        couple_oid=created_couple.oid,
        second_user_oid=faker.pystr(),
    )

    with pytest.raises(CoupleAlreadyHasSecondUserException):
        await unit_mediator.handle_command(command=command)

    assert len(created_couple._events) == 0, f'{created_couple=}'


@pytest.mark.asyncio
async def test_form_couple_command_handler_same_user(
    couple_repo: BaseCouplesRepository,
    unit_mediator: Mediator,
):
    couple: Couple = CoupleEntityFactory.create()
    created_couple: Couple = await couple_repo.create(couple=couple)
    command: FormCoupleCommand = FormCoupleCommand(
        couple_oid=created_couple.oid,
        second_user_oid=created_couple.first_user_oid,
    )

    with pytest.raises(CannotAddSameUserToCoupleException):
        await unit_mediator.handle_command(command=command)

    assert len(created_couple._events) == 0, f'{created_couple=}'
