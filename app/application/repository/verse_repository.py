from abc import ABC, abstractmethod
from typing import List

from app.domain.entity.verse_entity import VerseEntity


class VerseRepository(ABC):
    @abstractmethod
    def get_all() -> List[VerseEntity]:
        pass

    @abstractmethod
    def get_by_verse_id(self, verse_id) -> VerseEntity:
        pass
