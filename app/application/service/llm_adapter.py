from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generator

from app.domain.value_object.llm_stream import LLMStream


class LLMAdapter(ABC):
    @abstractmethod
    def setup(self, type: str):
        pass

    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        pass

    @abstractmethod
    def generate_stream(
        self, prompt: str, max_tokens: int
    ) -> Generator[LLMStream, str, None]:
        pass


@dataclass
class LLMCollection:
    general: LLMAdapter
    intent_classifier: LLMAdapter
    paraphrase: LLMAdapter
