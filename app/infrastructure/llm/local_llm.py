from typing import Literal

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from app.application.service.llm_adapter import LLMAdapter


class LocalLLM(LLMAdapter):
    def __init__(
        self,
        model_id: Literal[
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "google/gemma-3-1b-it",
            "google/gemma-2b-it",
            "mistralai/Mistral-7B-Instruct-v0.1",
        ],
    ):
        self.model_id = model_id
        self.tokenizer = None
        self.model = None

    def setup(self, type: str):
        print("Loading", self.model_id, type)

        if not self.tokenizer:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)

        if not self.model:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                torch_dtype=(
                    torch.float16 if torch.cuda.is_available() else torch.float32
                ),
            )
            self.model.eval()

    def generate(self, prompt: str, max_tokens=256):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=max_tokens)
        return self.__clean_response(
            self.tokenizer.decode(outputs[0], skip_special_tokens=True).replace(
                prompt, ""
            )
        )

    def generate_stream(self, prompt: str, max_tokens=256):
        raise NotImplementedError()

    def __clean_response(self, response: str):
        return response.replace("<br>", "").replace("```", "").strip("")
