from abc import ABC, abstractmethod
from typing import List

from rich.console import Console  # harmfull

from app.application.repository.chapter_repository import ChapterRepository
from app.application.repository.verse_repository import VerseRepository
from app.application.repository.gita_repository import (
    GitaRepository,
)
from app.application.service.llm_adapter import LLMCollection
from app.application.service.pattern_matching import PatternMatching
from app.application.service.searcher import Searcher
from app.domain.entity.chapter_entity import ChapterEntity
from app.domain.entity.gita_entity import GitaEntity
from app.domain.value_object.pattern_matching_result import PatternMatchingResult


class ApplicationConstruct(ABC):
    def __init__(
        self,
        llm_collection: LLMCollection,
        chapter_repository: ChapterRepository,
        verse_repository: VerseRepository,
        gita_repository: GitaRepository,
        chapter_searcher: Searcher,
        gita_searcher: Searcher,
        pattern_matching_services: List[PatternMatching],
    ):
        self.console = Console()
        self.llm_collection = llm_collection
        self.chapter_repository = chapter_repository
        self.verse_repository = verse_repository
        self.gita_repository = gita_repository
        self.chapter_searcher = chapter_searcher
        self.gita_searcher = gita_searcher
        self.pattern_matching_services = pattern_matching_services

    def prepare_model(self):
        # Load chapter model
        self.console.print("[blue][INFO][/blue] Memuat model [b]chapter[/b]...")
        if self.chapter_searcher.builded():
            self.chapter_searcher.load_index()
        else:
            self.chapter_searcher.build_index(self.chapter_repository.get_all())
        # self.console.print('Chapter searcher loaded!', style='bold green')

        # Load verse translation model
        self.console.print(
            "[blue][INFO][/blue] Memuat model [b]verse translation[/b]..."
        )
        if self.gita_searcher.builded():
            self.gita_searcher.load_index()
        else:
            self.gita_searcher.build_index(self.gita_repository.get_all())

    def get_context(
        self, user_input: str
    ) -> List[ChapterEntity] | List[GitaEntity] | PatternMatchingResult | None:
        results = None
        for pattern_matching_service in self.pattern_matching_services:
            matching_result = pattern_matching_service.match(user_input)
            if matching_result:
                results = pattern_matching_service.handle(
                    self.llm_collection.general, user_input, matching_result
                )
                break

        if not results:
            if "bab" in user_input.lower():
                self.console.print(
                    "[yellow][AI][/yellow] Menggunakan model [b]chapter translation[/b]..."
                )
                results = self.chapter_searcher.search(user_input)
            else:
                self.console.print(
                    "[yellow][AI][/yellow] Menggunakan model [b]verse translation[/b]..."
                )
                results = self.gita_searcher.search(user_input)

        return results

    @abstractmethod
    def run(self):
        pass
