from dataclasses import dataclass, field

from src.domain.entities.couples import Couple
from src.infrastructure.repositories.couples.base import BaseCouplesRepository


@dataclass
class MemoryCouplesRepository(BaseCouplesRepository):
    _cuoples: list[Couple] = field(
        default_factory=list,
        kw_only=True,
    )

    async def create(self, couple: Couple) -> Couple:
        self._cuoples.append(couple)
        return couple

    async def get_by_oid(self, oid: str) -> Couple | None:
        try:
            return next(couple for couple in self._cuoples if couple.oid == oid)

        except StopIteration:
            return None

    async def update_by_oid(self, oid: str, couple: Couple) -> bool:
        for index, couple in enumerate(self._cuoples):
            if couple.oid == oid:
                self._cuoples.pop(index)
                self._cuoples.append(couple)
                return True

        return False
