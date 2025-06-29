from dataclasses import dataclass, field
from typing import List, Literal

ResultType = Literal["context", "direct"]


@dataclass
class PatternMatchingContext:
    label: str
    content: str
    link: str | None = None


@dataclass
class PatternMatchingResult:
    type: ResultType = "direct"
    output: str = ""
    context: List[PatternMatchingContext] = field(default_factory=list)
