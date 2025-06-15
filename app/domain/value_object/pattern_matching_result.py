from dataclasses import dataclass
from typing import Generic, List, TypeVar

T = TypeVar("T")


@dataclass
class PatternMatchingResult(Generic[T]):
    output: str
    attachments: List[T]
