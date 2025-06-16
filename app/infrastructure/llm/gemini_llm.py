from typing import Literal

import google.generativeai as genai
from rich.console import Console

from app.application.service.llm_adapter import LLMAdapter
from app.domain.value_object.llm_stream import LLMStream


class GeminiLLM(LLMAdapter):
    def __init__(self, model_id: Literal["gemini-2.0-flash"], api_key: str):
        self.console = Console()
        self.model_id = model_id
        self.__API_KEY = api_key
        self.model = None

    def setup(self, type: str):
        self.console.print(
            f"[blue][INFO][/blue] Menggunakan model [b]{self.model_id}[/b] for {type}"
        )

        genai.configure(api_key=self.__API_KEY)
        # Load model
        self.model = genai.GenerativeModel(self.model_id)

    def generate(self, prompt: str, max_tokens=256):
        result = self.model.generate_content(prompt)
        return result.text

    def generate_stream(self, prompt: str, max_tokens=256):
        response = self.generate(prompt, max_tokens)
        yield LLMStream(model=self.model_id, content_chunk=response)
