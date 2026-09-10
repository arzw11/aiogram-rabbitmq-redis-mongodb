from dataclasses import dataclass

from src.domain.commands.base import BaseCommand


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    telegram_id: int
    name: str


@dataclass(frozen=True)
class GetUserByOIDCommand(BaseCommand):
    oid: str


@dataclass(frozen=True)
class GetUserByTelegramIDCommand(BaseCommand):
    telegram_id: int
