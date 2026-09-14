import copy

import pytest
from faker import Faker
from tests.factories.couples import CoupleEntityFactory

from src.domain.entities.couples import Couple
from src.infrastructure.repositories.couples.base import BaseCouplesRepository


@pytest.mark.asyncio
async def test_couple_repo_create(couple_repo: BaseCouplesRepository):
    couple: Couple = CoupleEntityFactory.create()
    created_couple: Couple = await couple_repo.create(couple)

    assert created_couple == couple, f'{created_couple=}'


@pytest.mark.asyncio
async def test_couple_repo_create_batch(faker: Faker, couple_repo: BaseCouplesRepository):
    size = faker.pyint(min_value=0, max_value=10)
    couples: list[Couple] = CoupleEntityFactory.create_batch(size=size)
    created_couples: list[Couple] = [await couple_repo.create(couple) for couple in couples]

    assert len(created_couples) == size, f'{created_couples=}'


@pytest.mark.asyncio
async def test_couple_repo_get_by_oid(couple_repo: BaseCouplesRepository):
    couple: Couple = CoupleEntityFactory.create()
    await couple_repo.create(couple)

    fetched_couple: Couple = await couple_repo.get_by_oid(oid=couple.oid)

    assert fetched_couple == couple, f'{fetched_couple=}'


@pytest.mark.asyncio
async def test_couple_repo_get_by_oid_none(faker: Faker, couple_repo: BaseCouplesRepository):
    fetched_couple: None = await couple_repo.get_by_oid(oid=faker.text(max_nb_chars=32))

    assert not fetched_couple, f'{fetched_couple=}'


@pytest.mark.asyncio
async def test_couple_repo_update_by_oid(faker: Faker, couple_repo: BaseCouplesRepository):
    couple: Couple = CoupleEntityFactory.create()
    await couple_repo.create(couple=couple)

    copy_couple = copy.deepcopy(couple)
    copy_couple.title = faker.text(max_nb_chars=64)

    result: bool = await couple_repo.update_by_oid(oid=couple.oid, couple=copy_couple)

    assert result, f'{result=}'


@pytest.mark.asyncio
async def test_couple_repo_update_by_oid_false(couple_repo: BaseCouplesRepository):
    couple: Couple = CoupleEntityFactory.create()

    result: bool = await couple_repo.update_by_oid(oid=couple.oid, couple=couple)

    assert not result, f'{result=}'
