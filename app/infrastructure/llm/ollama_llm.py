from typing import Literal

import ollama
from rich.console import Console

from app.application.service.llm_adapter import LLMAdapter
from app.domain.value_object.llm_stream import LLMStream


class OllamaLLM(LLMAdapter):
    def __init__(self, model_id: Literal["deepseek-r1:7b"]):
        self.console = Console()
        self.model_id = model_id

    def setup(self, type: str):
        self.console.print(
            f"[blue][INFO][/blue] Menggunakan model [b]{self.model_id}[/b] for {type}"
        )

    def generate(self, prompt: str, max_tokens=256):
        result = ollama.chat(
            model=self.model_id,
            messages=[{"role": "user", "content": prompt}],
        )

        return result.message.content

    def generate_stream(self, prompt: str, max_tokens=256):
        result: ollama.ChatResponse = ollama.chat(
            model=self.model_id,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Jawab pertanyaan yang diberikan"},
            ],
            stream=True,
            think=False,
            # max_tokens=max_tokens
        )

        for chunk in result:
            yield LLMStream(model=chunk.model, content_chunk=chunk.message.content)
