from abc import ABC, abstractmethod
from typing import List

from app.application.application_container import ApplicationContainer

from rich.console import Console  # harmfull
from app.domain.entity.chapter_entity import ChapterEntity
from app.domain.entity.gita_entity import GitaEntity, MixedGitaEntity
from app.domain.value_object.pattern_matching_result import PatternMatchingResult


class ApplicationConstruct(ABC):
    def __init__(
        self,
        app: ApplicationContainer,
    ):
        self.console = Console()
        self.app: ApplicationContainer = app

    def prepare_model(self):
        self.app.llm_collection.general.setup("general")
        self.app.llm_collection.intent_classifier.setup("intent_classifier")
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

    def prepare_matcher(self):
        for matcher in self.app.pattern_matching_services:
            matcher.set_app(self.app)

    def get_context(
        self, user_input: str
    ) -> List[GitaEntity | MixedGitaEntity] | PatternMatchingResult | None:
        results = None
        for pattern_matching_service in self.app.pattern_matching_services:
            matching_result = pattern_matching_service.match(user_input)
            if matching_result:
                results = pattern_matching_service.handle(user_input, matching_result)
                if results:
                    break

        if not results:
            self.console.print(
                "[yellow][AI][/yellow] Menggunakan model [b]FULL GITA SEARCH[/b]..."
            )
            results = self.app.gita_searcher.search(user_input)

        return results

    @abstractmethod
    def run(self):
        pass
