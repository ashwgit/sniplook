import logging
from dataclasses import dataclass, field

from src.errors import ModelLoadError

logger = logging.getLogger(__name__)


@dataclass
class SnippetBase:
    content: str
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not isinstance(self.content, str):
            logger.error("Currently does not support anything other than text.")
            raise ModelLoadError("Snippet content must be string.")


class SnippetCreate(SnippetBase):
    pass


@dataclass
class SnippetInDB(SnippetBase):
    id: int
    tags: list[str]

    def __hash__(self):
        return hash((self.content))

    def __eq__(self, other):
        if not isinstance(other, SnippetBase):
            return False
        return self.content == other.content
