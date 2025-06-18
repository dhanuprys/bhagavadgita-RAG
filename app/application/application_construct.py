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
from app.application.service.prompt_builder import PromptBuilder
from app.domain.entity.chapter_entity import ChapterEntity
from app.domain.entity.gita_entity import GitaEntity, MixedGitaEntity
from app.domain.value_object.pattern_matching_result import PatternMatchingResult

from dataclasses import dataclass


@dataclass
class ApplicationContainer:
    llm_collection: LLMCollection
    chapter_repository: ChapterRepository
    verse_repository: VerseRepository
    gita_repository: GitaRepository
    chapter_searcher: Searcher
    gita_searcher: Searcher
    prompt_builder: PromptBuilder
    pattern_matching_services: List[PatternMatching]


class ApplicationConstruct(ABC):
    def __init__(
        self,
        app: ApplicationContainer,
    ):
        self.console = Console()
        self.app: ApplicationContainer = app

    def prepare_model(self):
        self.app.llm_collection.general.setup("general")
        self.app.llm_collection.context_focused.setup("context_focused")
        self.app.llm_collection.paraphrase.setup("paraphrase")

        # Load chapter model
        self.console.print("[blue][INFO][/blue] Memuat model [b]chapter[/b]...")
        chapters = self.app.chapter_repository.get_all()
        if self.app.chapter_searcher.builded():
            self.app.chapter_searcher.load_index()
        else:
            self.app.chapter_searcher.build_index(chapters)
        self.console.print(
            f"[blue][INFO][/blue] Berhasil memuat {len(chapters)} baris data."
        )

        # Load verse translation model
        self.console.print(
            "[blue][INFO][/blue] Memuat model [b]verse translation[/b]..."
        )
        complete_gita = self.app.gita_repository.get_all()
        if self.app.gita_searcher.builded():
            self.app.gita_searcher.load_index()
        else:
            self.app.gita_searcher.build_index(complete_gita)
        self.console.print(
            f"[blue][INFO][/blue] Berhasil memuat {len(complete_gita)} baris data."
        )

    def get_context(
        self, user_input: str
    ) -> (
        List[ChapterEntity]
        | List[GitaEntity | MixedGitaEntity]
        | PatternMatchingResult
        | None
    ):
        results = None
        for pattern_matching_service in self.app.pattern_matching_services:
            matching_result = pattern_matching_service.match(user_input)
            if matching_result:
                results = pattern_matching_service.handle(
                    self.app.llm_collection, user_input, matching_result
                )
                break

        if not results:
            if "bab" in user_input.lower():
                self.console.print(
                    "[yellow][AI][/yellow] Menggunakan model [b]chapter translation[/b]..."
                )
                results = self.app.chapter_searcher.search(user_input)
            else:
                self.console.print(
                    "[yellow][AI][/yellow] Menggunakan model [b]verse translation[/b]..."
                )
                results = self.app.gita_searcher.search(user_input)

        return results

    @abstractmethod
    def run(self):
        pass
