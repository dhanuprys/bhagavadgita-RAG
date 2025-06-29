from abc import ABC, abstractmethod
from typing import List

from app.domain.entity.gita_entity import GitaEntity


class GitaRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[GitaEntity]:
        pass
