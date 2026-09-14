import asyncio
from dataclasses import dataclass, field
from typing import AsyncIterator

import orjson
from aio_pika import ExchangeType
from aiormq import Channel, Connection

from src.infrastructure.exceptions.message_brokers import ChannelNotInitedException
from src.infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class RabbitMessageBroker(BaseMessageBroker):
    connection: Connection
    _channel: Channel | None = field(default=None, kw_only=True)

    @property
    def channel(self) -> Channel:
        if self._channel is None or self._channel.is_closed:
            raise ChannelNotInitedException()
        return self._channel

    async def _setup(self) -> None:
        if self._channel is None or self._channel.is_closed:
            self._channel = await self.connection.channel()

        channel = self.channel

        await channel.exchange_declare(exchange="users_exchange", exchange_type=ExchangeType.TOPIC.value, durable=True)
        await channel.queue_declare(queue="users_queue", durable=True)
        await channel.queue_bind(queue="users_queue", exchange="users_exchange", routing_key="events.#")

    async def start(self) -> None:
        await self._setup()

    async def send_message(self, topic: str, key: str, value: bytes) -> None:
        await self.channel.basic_publish(body=value, exchange=topic, routing_key=key)

    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        while True:
            message = await self.channel.basic_get(queue=topic, no_ack=False)

            if message is not None and message.delivery_tag is not None:
                await self.channel.basic_ack(message.delivery_tag)
                yield orjson.loads(message.body)

            await asyncio.sleep(0.1)

    async def stop_consuming(self, topic: str) -> None: ...

    async def close(self) -> None:
        await self.channel.close()
        await self.connection.close()
