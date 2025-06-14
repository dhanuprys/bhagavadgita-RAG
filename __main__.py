from app.infrastructure.llm.local_llm import LocalLLM
from app.infrastructure.repository.json_chapter_repository import JsonChapterRepository
from app.infrastructure.repository.json_verse_repository import JsonVerseRepository
from app.infrastructure.repository.json_verse_translation_repository import JsonVerseTranslationRepository
from app.infrastructure.searcher.verse_translation_searcher import VerseTranslationSearcher
from app.infrastructure.searcher.chapter_searcher import ChapterSearcher
from app.application.service.llm_adapter import LLMCollection
from app.infrastructure.matcher.chapter_matching import ChapterMatching
from app.infrastructure.cli_app import CLIApp

def main():
    llm = LocalLLM('google/gemma-3-1b-it')
    app = CLIApp(
        # THIS IS INSTANCE ONLY CAN USE ONE LLM INSTANCE DUE TO OOM
        llm_collection=LLMCollection(
            general=llm,
            context_focused=llm,
            paraphrase=llm
        ),
        chapter_repository=JsonChapterRepository(),
        verse_repository=JsonVerseRepository(),
        verse_translation_repository=JsonVerseTranslationRepository(),
        chapter_searcher=ChapterSearcher(),
        verse_translation_searcher=VerseTranslationSearcher(),
        pattern_matching_services=[
            # Bab 1, Bab 2
            ChapterMatching()
        ]
    )
    print("Starting app")
    app.run()
    
if __name__ == "__main__":
    main()