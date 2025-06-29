from abc import ABC, abstractmethod


class Searcher(ABC):
    @abstractmethod
    def builded(self) -> bool:
        pass

    @abstractmethod
    def build_index(self, data) -> bool:
        pass

    @abstractmethod
    def load_index(self) -> bool:
        pass

    @abstractmethod
    def search(self, query: str):
        pass
