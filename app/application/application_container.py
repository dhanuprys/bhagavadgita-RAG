from dataclasses import dataclass
from typing import List

from app.application.repository.chapter_repository import ChapterRepository
from app.application.repository.verse_repository import VerseRepository
from app.application.repository.verse_translation_repository import (
    VerseTranslationRepository,
)
from app.application.repository.gita_repository import (
    GitaRepository,
)
from app.application.service.llm_adapter import LLMCollection
from app.application.service.pattern_matching import PatternMatching
from app.application.service.searcher import Searcher
from app.application.service.prompt_builder import PromptBuilder


@dataclass
class ApplicationContainer:
    llm_collection: LLMCollection
    chapter_repository: ChapterRepository
    verse_repository: VerseRepository
    verse_translation_repository: VerseTranslationRepository
    gita_repository: GitaRepository
    chapter_searcher: Searcher
    gita_searcher: Searcher
    prompt_builder: PromptBuilder
    pattern_matching_services: List[PatternMatching]
