from typing import Literal, List

from google import genai
from rich.console import Console

from app.application.service.llm_adapter import LLMAdapter
from app.domain.value_object.llm_stream import LLMStream


class GeminiLLM(LLMAdapter):
    def __init__(
        self,
        model_id: Literal["gemini-2.0-flash", "gemini-2.5-flash"],
        api_keys: List[str],
    ):
        self.console = Console()
        self.model_id = model_id
        self.__API_KEY_ROTATION_INDEX = 0
        self.__API_KEY_LENGTH = len(api_keys)
        self.__API_KEYS = api_keys

    def setup(self, type: str):
        self.console.print(
            f"[blue][INFO][/blue] Menggunakan model [b]{self.model_id}[/b] for {type}"
        )

        # Load model
        self.__refresh_client()

    def generate(self, prompt: str, max_tokens=256):
        self.__refresh_client()

        result = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
        )

        return result.text or ""

    def generate_stream(self, prompt: str, max_tokens=256):
        response = self.generate(prompt, max_tokens)
        yield LLMStream(model=self.model_id, content_chunk=response or "")

    def __refresh_client(self):
        self.client: genai.Client = genai.Client(api_key=self.__API_KEY)

    def __rotate_api_key(self):
        self.__API_KEY_ROTATION_INDEX += 1
        if self.__API_KEY_ROTATION_INDEX >= self.__API_KEY_LENGTH:
            self.__API_KEY_ROTATION_INDEX = 0
        print("Using GEMINI KEY INDEX:", self.__API_KEY_ROTATION_INDEX)
        return self.__API_KEYS[self.__API_KEY_ROTATION_INDEX]

    @property
    def __API_KEY(self):
        return self.__rotate_api_key()
