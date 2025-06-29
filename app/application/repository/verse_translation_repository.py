from abc import ABC, abstractmethod
from typing import List

from app.domain.entity.verse_translation_entity import VerseTranslationEntity


class VerseTranslationRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_chapter_verse_number(
        self, chapter_number: int, verse_number: int
    ) -> List[VerseTranslationEntity]:
        pass

    @abstractmethod
    def get_by_verse_id(self, verse_id: int) -> List[VerseTranslationEntity]:
        pass
