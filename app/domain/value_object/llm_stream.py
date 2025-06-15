from dataclasses import dataclass

@dataclass
class LLMStream:
    model: str
    content_chunk: str