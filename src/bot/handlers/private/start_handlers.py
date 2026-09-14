import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import punq

from src.domain.commands.users import CreateUserCommand, GetUserByTelegramIDCommand
from src.services.mediator.base import Mediator

router = Router()


logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start_handler(message: Message, container: punq.Container) -> None:
    mediator: Mediator = container.resolve(Mediator)
    telegram_id: int = message.from_user.id

    fetched_user, *_ = await mediator.handle_command(
        command=GetUserByTelegramIDCommand(telegram_id=telegram_id),
    )

    if fetched_user is None:
        created_user, *_ = await mediator.handle_command(
            command=CreateUserCommand(telegram_id=telegram_id, name=message.from_user.username),
        )

        return await message.answer(text='Заргестрирован! Поздарвляю!')

    return await message.answer(text='Приветствую!')
