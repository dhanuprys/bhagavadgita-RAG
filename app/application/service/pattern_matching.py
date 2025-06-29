from abc import ABC, abstractmethod

from app.application.application_construct import ApplicationConstruct
from app.domain.value_object.pattern_matching_result import PatternMatchingResult


class PatternMatching(ABC):
    def set_ctx(self, ctx: ApplicationConstruct):
        self.ctx = ctx

    @abstractmethod
    def match(self, user_input: str) -> None | dict:
        pass

    @abstractmethod
    def handle(self, user_input: str, matching_result: dict) -> PatternMatchingResult:
        pass
