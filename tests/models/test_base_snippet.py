from unittest import TestCase, main

from src.errors import ModelLoadError
from src.models.base_snippet import SnippetBase


class TestModelSnippetBase(TestCase):
    def test_valid_model(self):
        snippet = SnippetBase(content="Hello, World!", tags=["Greet"])
        self.assertIsInstance(snippet.content, str)
        self.assertIsInstance(snippet.tags, list)

    def test_invalid_model(self):
        with self.assertRaises(ModelLoadError):
            SnippetBase(content=int(9), tags=["number"])


if __name__ == "__main__":
    main()
