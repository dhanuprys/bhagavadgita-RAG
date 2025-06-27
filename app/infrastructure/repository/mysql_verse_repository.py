from app.domain.entity.verse_entity import VerseEntity
from app.application.repository.verse_repository import VerseRepository
from app.infrastructure.dbclient.mysql_client import MysqlClient


class MysqlVerseRepository(VerseRepository):
    def __init__(self):
        self.client = MysqlClient()

    def get_all(self):
        result = self.client.query(
            """
            SELECT * FROM verses;
            """
        )

        return [VerseEntity(**row) for row in result]

    def get_by_chapter_number(self, chapter_number: int):
        result = self.client.query(
            """
            SELECT * FROM verses WHERE chapter_id = (SELECT id FROM chapters WHERE chapter_number = %s);
            """,
            (chapter_number,),
        )

        return [VerseEntity(**row) for row in result]

    def get_by_chapter_verse_number(
        self, chapter_number: int, verse_number: int
    ) -> VerseEntity:
        result = self.client.query(
            """
            SELECT * FROM verses WHERE verse_number = %s AND chapter_id = (SELECT id FROM chapters WHERE chapter_number = %s);
            """,
            (verse_number, chapter_number),
        )

        return VerseEntity(**result[0]) if result else None

    def get_by_verse_id(self, verse_id):
        raise NotImplementedError()
