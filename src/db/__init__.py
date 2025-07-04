from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.base_snippet import SnippetCreate, SnippetInDB


class Database(ABC):
    """Abstract base class for all database implementations"""

    @abstractmethod
    def create_snippet(self, snippet: SnippetCreate) -> SnippetInDB:
        pass

    @abstractmethod
    def get_snippet(self, snippet_id: int) -> Optional[SnippetInDB]:
        pass

    @abstractmethod
    def search_snippets(self, query: str, limit: int = 10) -> List[SnippetInDB]:
        pass
