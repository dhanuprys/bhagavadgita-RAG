from app.application.service.pattern_matching import PatternMatching
from app.application.service.llm_adapter import LLMCollection
from app.domain.value_object.pattern_matching_result import PatternMatchingResult

class ChapterMatching(PatternMatching):
    def match(self, text: str) -> dict | None:
        # Simple regex to find chapter numbers (e.g., "Chapter 1", "Chap. 2", "Ch 3")
        # This is a basic example and might need refinement based on actual text patterns
        import re
        match = re.search(r'(?:Bab)\s*(\d+)', text, re.IGNORECASE)
        if match:
            print(f"Chapter {match.group(1)}")
            return {
                "chapter": match.group(1)
            }
        return None
    
    def handle(self, llm_collection: LLMCollection, user_input: str, matching_result: dict) -> PatternMatchingResult:
        return PatternMatchingResult[str](
            output="Hello world!" + matching_result['chapter'],
            attachments=['Bab 1']
        )