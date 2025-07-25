from app.application.repository.gita_repository import GitaRepository
from app.domain.entity.gita_entity import GitaEntity
from app.infrastructure.dbclient.mysql_client import MysqlClient

from typing import List


class MysqlGitaRepository(GitaRepository):
    def __init__(self, client: MysqlClient):
        self.client = client

    def get_all(self) -> List[GitaEntity]:
        result = self.client.query(
            """
            SELECT
              vt.id AS `vt_id`,
              vt.content AS `vt_content`,
              v.id AS `v_id`,
              v.text_sanskrit AS `v_text_sanskrit`,
              v.text_sanskrit_meanings AS `v_text_sanskrit_meanings`,
              v.verse_number AS `v_verse_number`,
              v.audio_url AS `v_audio_url`,
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

    def get_random_verses(self, count: int) -> List[GitaEntity]:
        result = self.client.query(
            """
            SELECT
              vt.id AS `vt_id`,
              vt.content AS `vt_content`,
              v.id AS `v_id`,
              v.text_sanskrit AS `v_text_sanskrit`,
              v.text_sanskrit_meanings AS `v_text_sanskrit_meanings`,
              v.verse_number AS `v_verse_number`,
              v.audio_url AS `v_audio_url`,
              c.id AS `c_id`,
              c.chapter_number AS `c_chapter_number`,
              c.name AS `c_name`,
              c.summary AS `c_summary`,
              c.verses_count AS `c_verses_count`
            FROM
              verses v
              LEFT JOIN (
                SELECT vt.*
                FROM verse_translations vt
                INNER JOIN (
                  SELECT verse_id, MIN(id) AS min_id
                  FROM verse_translations
                  GROUP BY verse_id
                ) filtered ON vt.id = filtered.min_id
              ) vt ON vt.verse_id = v.id
              INNER JOIN chapters c ON c.id = v.chapter_id
            ORDER BY RAND()
            LIMIT %s;
            """,
            (count,),
        )

        return [GitaEntity(**row) for row in result]

    def get_sample_verses(self, chapter: int, count: int) -> List[GitaEntity]:
        result = self.client.query(
            """
            SELECT
              vt.id AS `vt_id`,
              vt.content AS `vt_content`,
              v.id AS `v_id`,
              v.text_sanskrit AS `v_text_sanskrit`,
              v.text_sanskrit_meanings AS `v_text_sanskrit_meanings`,
              v.verse_number AS `v_verse_number`,
              v.audio_url AS `v_audio_url`,
              c.id AS `c_id`,
              c.chapter_number AS `c_chapter_number`,
              c.name AS `c_name`,
              c.summary AS `c_summary`,
              c.verses_count AS `c_verses_count`
            FROM
              verses v
              LEFT JOIN (
                SELECT vt.*
                FROM verse_translations vt
                INNER JOIN (
                  SELECT verse_id, MIN(id) AS min_id
                  FROM verse_translations
                  GROUP BY verse_id
                ) filtered ON vt.id = filtered.min_id
              ) vt ON vt.verse_id = v.id
              INNER JOIN chapters c ON c.id = v.chapter_id
            WHERE c.chapter_number = %s
            ORDER BY RAND()
            LIMIT %s;
            """,
            (
                chapter,
                count,
            ),
        )

        return [GitaEntity(**row) for row in result]

    def get_specific_verse(self, chapter: int, verse: int) -> GitaEntity | None:
        result = self.client.query(
            """
            SELECT
              vt.id AS `vt_id`,
              vt.content AS `vt_content`,
              v.id AS `v_id`,
              v.text_sanskrit AS `v_text_sanskrit`,
              v.text_sanskrit_meanings AS `v_text_sanskrit_meanings`,
              v.verse_number AS `v_verse_number`,
              v.audio_url AS `v_audio_url`,
              c.id AS `c_id`,
              c.chapter_number AS `c_chapter_number`,
              c.name AS `c_name`,
              c.summary AS `c_summary`,
              c.verses_count AS `c_verses_count`
            FROM
              verse_translations vt
              INNER JOIN verses v ON v.id = vt.verse_id
              INNER JOIN chapters c ON c.id = v.chapter_id
            WHERE v.verse_number = %s AND c.chapter_number = %s;
            """,
            (verse, chapter),
        )

        return GitaEntity(**result[0]) if result else None
