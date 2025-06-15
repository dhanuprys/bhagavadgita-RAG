from app.infrastructure.llm.ollama_llm import OllamaLLM
from app.infrastructure.repository.json_chapter_repository import JsonChapterRepository
from app.infrastructure.repository.json_verse_repository import JsonVerseRepository
from app.infrastructure.repository.json_verse_translation_repository import JsonVerseTranslationRepository
from app.infrastructure.searcher.verse_translation_searcher import VerseTranslationSearcher
from app.infrastructure.searcher.chapter_searcher import ChapterSearcher
from app.application.service.llm_adapter import LLMCollection
from app.infrastructure.matcher.chapter_matching import ChapterMatching
from app.infrastructure.cli_app import CLIApp

def main():
    llm = OllamaLLM('deepseek-r1:7b')
    app = CLIApp(
        # ONLY CAN USE ONE LLM INSTANCE DUE TO Out-Of-Memory
        llm_collection=LLMCollection(
            general=llm,
            context_focused=llm,
            paraphrase=llm # LocalLLM('TinyLLM') x
        ),
        chapter_repository=JsonChapterRepository(),
        verse_repository=JsonVerseRepository(),
        verse_translation_repository=JsonVerseTranslationRepository(),
        chapter_searcher=ChapterSearcher(),
        verse_translation_searcher=VerseTranslationSearcher(),
        pattern_matching_services=[
            # Still on development
            # Bab 1, Bab 2
            ChapterMatching()
        ]
    )
    app.run()
    
if __name__ == "__main__":
    main()