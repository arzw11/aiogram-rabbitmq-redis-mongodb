from faker import Faker

from src.domain.entities.users import User
from src.domain.events.users import UserCreatedEvent


def test_create_user(faker: Faker) -> None:
    telegram_id = faker.random_int()
    name = faker.name()

    user: User = User.create_user(
        telegram_id=telegram_id,
        name=name,
    )

    assert user.telegram_id == telegram_id, f'{user=}'
    assert user.name == name, f'{user=}'
    assert isinstance(user._events[0], UserCreatedEvent)
