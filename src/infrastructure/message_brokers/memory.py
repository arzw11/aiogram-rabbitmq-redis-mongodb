import asyncio
from collections import defaultdict
from dataclasses import dataclass, field
from typing import AsyncIterator

import orjson

from src.infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class MemoryMessageBroker(BaseMessageBroker):
    _messages: dict[str, list[dict]] = field(default_factory=lambda: defaultdict(list), kw_only=True)
    _bindings: dict[str, str] = field(default_factory=dict, kw_only=True)

    async def start(self) -> None:
        self._bindings["users_queue"] = "events.#"

    async def close(self) -> None:
        self._messages.clear()
        self._bindings.clear()

    async def send_message(self, topic: str, key: str, value: bytes) -> None:
        for queue_name, pattern in self._bindings.items():
            if self._match_routing_key(key, pattern):
                self._messages[queue_name].append({"routing_key": key, "exchange": topic, "body": value})

    async def start_consuming(self, queue_name: str) -> AsyncIterator[dict]:
        while True:
            if self._messages[queue_name]:
                message = self._messages[queue_name].pop(0)
                yield {
                    "routing_key": message["routing_key"],
                    "exchange": message["exchange"],
                    "body": orjson.loads(message["body"]),
                }
            else:
                await asyncio.sleep(0.1)

    async def stop_consuming(self, topic: str) -> None: ...

    def _match_routing_key(self, routing_key: str, pattern: str) -> bool:
        if pattern == "#":
            return True

        pattern_parts = pattern.split(".")
        key_parts = routing_key.split(".")

        i = 0
        for part in pattern_parts:
            if part == "#":
                return True
            if part == "*":
                if i >= len(key_parts):
                    return False
                i += 1
            else:
                if i >= len(key_parts) or key_parts[i] != part:
                    return False
                i += 1

        return i == len(key_parts)
