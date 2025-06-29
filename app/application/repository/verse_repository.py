from abc import ABC, abstractmethod
from typing import List

from app.domain.entity.verse_entity import VerseEntity


class VerseRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[VerseEntity]:
        pass

    @abstractmethod
    def get_by_chapter_number(self, chapter_number) -> List[VerseEntity]:
        pass

    @abstractmethod
    def get_random(self, count: int) -> List[VerseEntity]:
        pass

    @abstractmethod
    def get_by_chapter_verse_number(self, chapter_number, verse_number) -> VerseEntity:
        pass

    @abstractmethod
    def get_by_verse_id(self, verse_id) -> VerseEntity:
        pass
