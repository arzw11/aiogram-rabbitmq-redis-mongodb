from dataclasses import dataclass

from src.domain.commands.couples import CreateCoupleCommand, FormCoupleCommand, GetCoupleByOIDCommand
from src.domain.entities.couples import Couple
from src.infrastructure.repositories.couples.base import BaseCouplesRepository
from src.services.handlers.commands.base import CommandHandler


@dataclass(frozen=True)
class CreateCoupleCommandHandler(CommandHandler[CreateCoupleCommand, Couple]):
    couples_repository: BaseCouplesRepository

    async def handle(self, command: CreateCoupleCommand) -> Couple:
        couple: Couple = Couple.create_couple(
            title=command.title,
            first_user_oid=command.first_user_oid,
        )
        created_couple: Couple = await self.couples_repository.create(couple=couple)

        return created_couple


@dataclass(frozen=True)
class GetCoupleByOIDCommandHandler(CommandHandler[GetCoupleByOIDCommand, Couple | None]):
    couples_repository: BaseCouplesRepository

    async def handle(self, command: GetCoupleByOIDCommand) -> Couple | None:
        return await self.couples_repository.get_by_oid(oid=command.couple_oid)


@dataclass(frozen=True)
class FormCoupleCommandHandler(CommandHandler[FormCoupleCommand, bool]):
    couples_repository: BaseCouplesRepository

    async def handle(self, command: FormCoupleCommand) -> bool:
        couple: Couple | None = await self.couples_repository.get_by_oid(oid=command.couple_oid)

        if couple is None:
            return False

        couple.add_second_user(second_user_oid=command.second_user_oid)
        return await self.couples_repository.update_by_oid(
            oid=command.couple_oid,
            couple=couple,
        )
