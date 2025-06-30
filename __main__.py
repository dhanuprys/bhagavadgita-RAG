from dotenv import load_dotenv
from os import getenv
import json
from typing import List

from app.application.service.llm_adapter import LLMCollection
from app.application.application_container import ApplicationContainer
from app.infrastructure.http.app import HttpApp
from app.infrastructure.llm.gemini_llm import GeminiLLM
from app.infrastructure.prompt.gemini_prompt import GeminiPrompt
from app.infrastructure.matcher.full_gita_matching import FullGitaMatching
from app.infrastructure.repository.mysql_chapter_repository import (
    MysqlChapterRepository,
)
from app.infrastructure.repository.mysql_verse_repository import MysqlVerseRepository
from app.infrastructure.repository.mysql_verse_translation_repository import (
    MysqlVerseTranslationRepository,
)
from app.infrastructure.repository.mysql_gita_repository import (
    MysqlGitaRepository,
)
from app.infrastructure.searcher.chapter_searcher import ChapterSearcher
from app.infrastructure.searcher.gita_searcher import (
    GitaSearcher,
)
from app.infrastructure.dbclient.mysql_client import MysqlClient

load_dotenv()


def main():
    env_gemini_keys = getenv("GEMINI_API_KEYS")

    if env_gemini_keys is None:
        print("Please set GEMINI_API_KEYS environment variable")
        exit()

    gemini_keys: List[str] = json.loads(env_gemini_keys)
    llm = GeminiLLM(
        "gemini-2.5-flash",
        gemini_keys,
    )
    llm_intent = GeminiLLM(
        "gemini-2.0-flash",
        gemini_keys,
    )

    mysql_client = MysqlClient()
    app_container = ApplicationContainer(
        # ONLY CAN USE ONE LLM INSTANCE DUE TO Out-Of-Memory
        llm_collection=LLMCollection(
            general=llm, intent_classifier=llm, paraphrase=llm
        ),
        chapter_repository=MysqlChapterRepository(client=mysql_client),
        verse_repository=MysqlVerseRepository(client=mysql_client),
        verse_translation_repository=MysqlVerseTranslationRepository(
            client=mysql_client
        ),
        gita_repository=MysqlGitaRepository(client=mysql_client),
        chapter_searcher=ChapterSearcher(),
        gita_searcher=GitaSearcher(),
        prompt_builder=GeminiPrompt(),
        pattern_matching_services=[
            # Still on development
            FullGitaMatching()
        ],
    )
    app = HttpApp(app=app_container)
    app.run()


if __name__ == "__main__":
    main()
