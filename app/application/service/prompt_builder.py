from abc import ABC, abstractmethod
from app.domain.entity.gita_entity import GitaEntity
from typing import List


class PromptBuilder(ABC):
    @abstractmethod
    def check_question_relativeness(self, question: str) -> str:
        pass

    @abstractmethod
    def generate_flexible_prompt(
        self, question: str, context_list: List[str], markdown: bool = False
    ) -> str:
        pass

    @abstractmethod
    def generate_global_gita_prompt(
        self, question: str, gita_list: List[GitaEntity], markdown: bool = False
    ) -> str:
        pass
