### This file is meant to organise the sqlite search function. BTW these functions are still not used. 

import logging
import sqlite3
from pathlib import Path

logger = logging.getHandlerByName(__name__)

from src.models.base_snippet import SnippetInDB


class SearchDatabase:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def _connection(self, db_path: Path):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        return conn

    def search_snippets(self, query: str, limit: int = 10) -> list[SnippetInDB]:
        with self._connection(self.db_path) as conn:
            try:
                # Clean and prepare the query for FTS5
                search_term = self._prepare_fts_query(query)
                rows = conn.execute(
                    """
                    SELECT s.* FROM snippets s
                    JOIN snippets_fts fts ON s.id = fts.rowid
                    WHERE fts.content MATCH ?
                    ORDER BY bm25(snippets_fts)
                    LIMIT ?
                    """,
                    (search_term, limit),
                ).fetchall()
                return [self._row_to_model(row) for row in rows]

            except sqlite3.OperationalError as e:
                logger.error(f"Search failed for query '{query}': {str(e)}")
                return []
