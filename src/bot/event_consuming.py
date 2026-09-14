import asyncio
import logging

import punq

from src.infrastructure.message_brokers.base import BaseMessageBroker
from src.project.containers import get_container

logger = logging.getLogger(__name__)


async def start_message_broker() -> None:
    container: punq.Container = get_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)

    await message_broker.start()
    logger.info('Message Broker запустился.')


async def consume_in_background():
    container: punq.Container = get_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)

    asyncio.create_task(consume_users_console(message_broker))


async def consume_users_console(message_broker: BaseMessageBroker):
    async for message in message_broker.start_consuming(topic='users_console'):
        logger.info('Событие получено. %s', message)


async def stop_message_broker() -> None:
    container: punq.Container = get_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)

    await message_broker.close()
    logger.info('Message Broker остановился.')
