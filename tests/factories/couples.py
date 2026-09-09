from uuid import uuid4

from factory.base import Factory
from factory.faker import Faker

from src.domain.entities.couples import Couple


class CoupleEntityFactory(Factory):
    title = Faker("text", max_nb_chars=64)
    first_user_oid = str(uuid4())

    class Meta:
        model = Couple
