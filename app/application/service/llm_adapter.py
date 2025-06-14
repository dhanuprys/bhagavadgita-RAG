from abc import ABC, abstractmethod
from dataclasses import dataclass

class LLMAdapter(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int) -> str:
        pass

@dataclass
class LLMCollection:
    general: LLMAdapter
    context_focused: LLMAdapter
    paraphrase: LLMAdapter
