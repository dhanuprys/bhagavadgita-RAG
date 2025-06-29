from abc import ABC, abstractmethod

from app.domain.value_object.pattern_matching_result import PatternMatchingResult
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.application.application_container import ApplicationContainer


class PatternMatching(ABC):
    def set_app(self, app: "ApplicationContainer"):
        self.app = app

    @abstractmethod
    def match(self, user_input: str) -> None | dict:
        pass

    @abstractmethod
    def handle(
        self, user_input: str, matching_result: dict
    ) -> PatternMatchingResult | None:
        pass
