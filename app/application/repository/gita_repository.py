from abc import ABC, abstractmethod
from typing import List

from app.domain.entity.gita_entity import GitaEntity


class GitaRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[GitaEntity]:
        pass

    @abstractmethod
    def get_random_verses(self, count: int) -> List[GitaEntity]:
        pass

    @abstractmethod
    def get_sample_verses(self, chapter: int, count: int) -> List[GitaEntity]:
        pass

    @abstractmethod
    def get_specific_verse(self, chapter: int, verse: int) -> GitaEntity | None:
        pass
