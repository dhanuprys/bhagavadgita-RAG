from dataclasses import dataclass, field
from typing import List, Literal

ResultType = Literal["context", "direct"]


@dataclass
class PatternMatchingContext:
    label: str
    content: str
    display_content: str = ""
    link: str | None = None

    def __post_init__(self):
        if not self.display_content:
            self.display_content = self.content


@dataclass
class PatternMatchingResult:
    type: ResultType = "direct"
    output: str = ""
    context: List[PatternMatchingContext] = field(default_factory=list)
