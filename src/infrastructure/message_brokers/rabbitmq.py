from dataclasses import dataclass, field
from typing import AsyncIterator

import aio_pika
import orjson

from src.infrastructure.exceptions.message_brokers import ChannelNotInitedException
from src.infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class RabbitMessageBroker(BaseMessageBroker):
    rabbitmq_uri: str
    _connection: aio_pika.Connection | None = field(default=None, kw_only=True)
    _channel: aio_pika.Channel | None = field(default=None, kw_only=True)

    async def _connect(self) -> None:
        self._connection = await aio_pika.connect(self.rabbitmq_uri)

    @property
    def channel(self) -> aio_pika.Channel:
        if self._channel is None or self._channel.is_closed:
            raise ChannelNotInitedException()
        return self._channel

    async def _setup(self) -> None:
        await self._connect()

        if self._channel is None or self._channel.is_closed:
            self._channel = await self._connection.channel()

        channel = self.channel

        users_exchange: aio_pika.Exchange = await channel.declare_exchange(
            name='users', type=aio_pika.ExchangeType.TOPIC, durable=True
        )
        users_queue: aio_pika.Queue = await channel.declare_queue(name='users_console', durable=True)

        await users_queue.bind(exchange=users_exchange, routing_key='events.#')

    async def start(self) -> None:
        await self._setup()

    async def send_message(self, topic: str, key: str, value: bytes) -> None:
        exchange: aio_pika.Exchange = await self.channel.get_exchange(name=topic)

        await exchange.publish(
            message=aio_pika.Message(value),
            routing_key=key,
        )

    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        queue: aio_pika.Queue = await self.channel.get_queue(name=topic)

        async with queue.iterator() as q_iter:
            async for message in q_iter:
                async with message.process():
                    yield orjson.loads(message.body)

    async def stop_consuming(self) -> None: ...

    async def close(self) -> None:
        if self._channel:
            await self._channel.close()

        if self._connection:
            await self._connection.close()
