from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseMessageBroker(ABC):
    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    async def send_message(self, topic: str, key: str, value: bytes) -> None: ...

    @abstractmethod
    async def start_consuming(self, topic: str) -> None: ...

    @abstractmethod
    async def stop_consuming(self, topic: str) -> None: ...
