from app.domain.value_object.pattern_matching_result import PatternMatchingResult
from app.application.service.llm_adapter import LLMCollection
from abc import ABC, abstractmethod

class PatternMatching(ABC):
    @abstractmethod
    def match(self, user_input: str) -> None | dict:
        pass
    
    @abstractmethod
    def handle(self, llm: LLMCollection, user_input: str, matching_result: dict) -> PatternMatchingResult:
        pass
