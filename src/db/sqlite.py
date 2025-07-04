import json
import logging
import re
import sqlite3
from pathlib import Path
from typing import Optional

from src.models.base_snippet import SnippetCreate, SnippetInDB

from . import Database

logger = logging.getLogger(__name__)


class SQLiteDatabase(Database):
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database"""
        self.db_path.parent.mkdir(exist_ok=True)
        with self._get_connection() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                tags_json TEXT DEFAULT '[]'
            )
            """)

            conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS snippets_fts 
            USING fts5(content, tags_json)
            """)

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create_snippet(self, snippet: SnippetCreate) -> SnippetInDB:
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO snippets 
                (content, tags_json)
                VALUES (?, ?)
                RETURNING id
                """,
                (
                    snippet.content.strip(),
                    json.dumps(snippet.tags),
                ),
            )
            snippet_id = cursor.fetchone()["id"]

            conn.execute(
                "INSERT INTO snippets_fts (rowid, content, tags_json) VALUES (?, ?, ?)",
                (snippet_id, snippet.content, json.dumps(snippet.tags)),
            )

            conn.commit()
            return self.get_snippet(snippet_id)

    def get_snippet(self, snippet_id: int) -> Optional[SnippetInDB]:
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM snippets WHERE id = ?", (snippet_id,)
            ).fetchone()
            return self._row_to_model(row) if row else None

    def search_snippets(self, query: str, limit: int = 10) -> set[SnippetInDB]:
        with self._get_connection() as conn:
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
                return set(self._row_to_model(row) for row in rows)

            except sqlite3.OperationalError as e:
                logger.error(f"Search failed for query '{query}': {str(e)}")
                return []

    def _prepare_fts_query(self, query: str) -> str:
        """Convert user query to valid FTS5 syntax"""
        # Remove problematic characters
        clean_query = re.sub(r"[^a-zA-Z0-9_*\s]", "", query).strip()

        if not clean_query:
            return ""

        # Handle wildcards and terms
        terms = []
        for term in clean_query.split():
            if term.endswith("*"):
                # Valid prefix wildcard
                terms.append(f"{term[:-1]}*")
            else:
                # Exact match or prefix search
                terms.append(f'"{term}" OR {term}*')

        return " OR ".join(terms)

    def _row_to_model(self, row) -> SnippetInDB:
        return SnippetInDB(
            id=row["id"],
            content=row["content"],
            tags=json.loads(row["tags_json"]),
        )

    def _get_data_for_remaining_id(
        self, id_to_exclude: list[int]
    ) -> list[SnippetInDB] | None:
        """
        Retrieve all snippets except those with IDs in the exclusion list.

        Args:
            id_to_exclude: List of snippet IDs to exclude from results

        Returns:
            List of SnippetInDB objects for remaining snippets, ordered by created_at (newest first).
            Returns None if no snippets found (or all are excluded).
        """
        if not id_to_exclude:
            with self._get_connection() as conn:
                rows = conn.execute(
                    """
                    SELECT * FROM snippets
                    """,
                ).fetchall()
                return [self._row_to_model(row) for row in rows]

        with self._get_connection() as conn:
            query = """
                SELECT * FROM snippets 
                WHERE id NOT IN ({})
            """.format(",".join(["?"] * len(id_to_exclude)))

            rows = conn.execute(query, id_to_exclude).fetchall()

            return [self._row_to_model(row) for row in rows] if rows else None
