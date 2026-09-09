from factory.base import Factory
from factory.faker import Faker

from src.domain.entities.users import User


class UserEntityFactory(Factory):
    telegram_id = Faker('random_int')
    name = Faker('name')

    class Meta:
        model = User
