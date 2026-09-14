from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.bot.event_consuming import consume_in_background, start_message_broker, stop_message_broker
from src.bot.handlers.private.start_handlers import router as start_handlers
from src.bot.middlewares.containers import ContainerMiddleware
from src.project.configs import settings


def create_bot() -> Bot:
    return Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def create_dispatcher() -> Dispatcher:
    dispatcher: Dispatcher = Dispatcher()

    # on startup
    dispatcher.startup.register(start_message_broker)
    dispatcher.startup.register(consume_in_background)

    # on shutdown
    dispatcher.shutdown.register(stop_message_broker)

    return dispatcher


def add_middleware(dispatcher: Dispatcher) -> None:
    dispatcher.update.middleware(ContainerMiddleware())


def add_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.include_router(router=start_handlers)


async def start_polling() -> None:
    bot: Bot = create_bot()
    dispatcher: Dispatcher = create_dispatcher()

    add_middleware(dispatcher=dispatcher)
    add_handlers(dispatcher=dispatcher)

    await dispatcher.start_polling(bot)
