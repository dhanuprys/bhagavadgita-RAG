from app.application.service.llm_adapter import LLMCollection
from app.application.application_construct import ApplicationContainer
from app.infrastructure.cli_app import CLIApp
from app.infrastructure.llm.ollama_llm import OllamaLLM
from app.infrastructure.llm.gemini_llm import GeminiLLM
from app.infrastructure.prompt.gemini_prompt import GeminiPrompt
from app.infrastructure.matcher.chapter_matching import ChapterMatching
from app.infrastructure.repository.json_chapter_repository import JsonChapterRepository
from app.infrastructure.repository.json_verse_repository import JsonVerseRepository
from app.infrastructure.repository.mysql_gita_repository import (
    MysqlGitaRepository,
)
from app.infrastructure.searcher.chapter_searcher import ChapterSearcher
from app.infrastructure.searcher.gita_searcher import (
    GitaSearcher,
)


def main():
    # JUST TAKE IT IF YOU WANT TO DO!!
    llm = GeminiLLM("gemini-2.0-flash", "AIzaSyCozswOipLBUxT2rUlRrMVvgAgrTmEZaOg")
    app_container = ApplicationContainer(
        # ONLY CAN USE ONE LLM INSTANCE DUE TO Out-Of-Memory
        llm_collection=LLMCollection(
            general=llm, context_focused=llm, paraphrase=llm  # LocalLLM('TinyLLM') x
        ),
        chapter_repository=JsonChapterRepository(),
        verse_repository=JsonVerseRepository(),
        gita_repository=MysqlGitaRepository(),
        chapter_searcher=ChapterSearcher(),
        gita_searcher=GitaSearcher(),
        prompt_builder=GeminiPrompt(),
        pattern_matching_services=[
            # Still on development
            # Bab 1, Bab 2
            ChapterMatching()
        ],
    )
    app = CLIApp(app=app_container)
    app.run()


if __name__ == "__main__":
    main()
