from dataclasses import dataclass

from src.domain.commands.base import BaseCommand


@dataclass(frozen=True)
class CreateCoupleCommand(BaseCommand):
    title: str
    first_user_oid: str


@dataclass(frozen=True)
class GetCoupleByOIDCommand(BaseCommand):
    couple_oid: str


@dataclass(frozen=True)
class FormCoupleCommand(BaseCommand):
    couple_oid: str
    second_user_oid: str
