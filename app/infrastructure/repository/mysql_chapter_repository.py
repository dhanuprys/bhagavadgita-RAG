from app.domain.entity.chapter_entity import ChapterEntity
from app.application.repository.chapter_repository import ChapterRepository
from app.infrastructure.dbclient.mysql_client import MysqlClient


class MysqlChapterRepository(ChapterRepository):
    def __init__(self, client: MysqlClient):
        self.client = client

    def get_all(self):
        result = self.client.query(
            """
            SELECT * FROM chapters;
            """
        )

        return [ChapterEntity(**row) for row in result]

    def get_chapter_by_number(self, chapter_number: int):
        result = self.client.query(
            """
            SELECT * FROM chapters WHERE chapter_number = %s;
            """,
            (chapter_number,),
        )

        return ChapterEntity(**result[0]) if result else None

    def get_chapter_by_id(self, chapter_id: int):
        result = self.client.query(
            """
            SELECT * FROM chapters WHERE id = %s;
            """,
            (chapter_id,),
        )

        return ChapterEntity(**result[0]) if result else None
