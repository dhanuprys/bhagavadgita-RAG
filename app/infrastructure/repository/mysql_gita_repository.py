from app.application.repository.gita_repository import GitaRepository
from app.domain.entity.gita_entity import GitaEntity
from app.infrastructure.dbclient.mysql_client import MysqlClient

from typing import List


class MysqlGitaRepository(GitaRepository):
    def __init__(self):
        self.client = MysqlClient()

    def get_all(self) -> List[GitaEntity]:
        result = self.client.query(
            """
            SELECT
              vt.id AS `vt_id`,
              vt.content AS `vt_content`,
              v.id AS `v_id`,
              v.text_sanskrit_meanings AS `v_text_sanskrit_meanings`,
              v.verse_number AS `v_verse_number`,
              c.id AS `c_id`,
              c.chapter_number AS `c_chapter_number`,
              c.name AS `c_name`,
              c.summary AS `c_summary`,
              c.verses_count AS `c_verses_count`
            FROM
              verse_translations vt
              INNER JOIN verses v ON v.id = vt.verse_id
              INNER JOIN chapters c ON c.id = v.chapter_id;
              """
        )

        return [GitaEntity(**row) for row in result]
