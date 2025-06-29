from typing import List
from app.domain.entity.verse_translation_entity import VerseTranslationEntity
from app.application.repository.verse_translation_repository import (
    VerseTranslationRepository,
)
from app.infrastructure.dbclient.mysql_client import MysqlClient


class MysqlVerseTranslationRepository(VerseTranslationRepository):
    def __init__(self, client: MysqlClient):
        self.client = client

    def get_all(self):
        result = self.client.query(
            """
            SELECT * FROM verse_translations;
            """
        )

        return [VerseTranslationEntity(**row) for row in result]

    def get_by_chapter_verse_number(
        self, chapter_number: int, verse_number: int
    ) -> List[VerseTranslationEntity]:
        result = self.client.query(
            """
            SELECT * FROM verse_translations WHERE verse_id IN (SELECT id FROM verses WHERE chapter_id = (SELECT id FROM chapters WHERE chapter_number = %s) AND verse_number = %s);
            """,
            (chapter_number, verse_number),
        )

        return [VerseTranslationEntity(**row) for row in result]

    def get_by_verse_id(self, verse_id: int) -> List[VerseTranslationEntity]:
        result = self.client.query(
            """
            SELECT * FROM verse_translations WHERE verse_id = %s;
            """,
            (verse_id,),
        )

        return [VerseTranslationEntity(**row) for row in result]
