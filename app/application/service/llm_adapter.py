from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generator

from app.domain.value_object.llm_stream import LLMStream


class LLMAdapter(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int) -> str:
        pass

    @abstractmethod
    def generate_stream(
        self, prompt: str, max_tokens: int
    ) -> Generator[LLMStream, any, None]:
        pass


@dataclass
class LLMCollection:
    general: LLMAdapter
    context_focused: LLMAdapter
    paraphrase: LLMAdapter
