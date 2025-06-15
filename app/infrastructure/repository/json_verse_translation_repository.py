from app.application.repository.verse_translation_repository import (
    VerseTranslationRepository,
)
from app.domain.entity.verse_translation_entity import VerseTranslationEntity
from app.infrastructure.util.json_loader import load_json


class JsonVerseTranslationRepository(VerseTranslationRepository):
    def __init__(self):
        self.db = []
        self.__load_data()

    def __load_data(self):
        data = load_json("data/3-fine-verse_number/translations.json")
        for verse_translation in data:
            self.db.append(VerseTranslationEntity(**verse_translation))

    def get_all(self):
        return self.db

    def get_by_verse_id(self, verse_id):
        for verse_translation in self.db:
            if verse_translation.verse_id == verse_id:
                return verse_translation
        return None
