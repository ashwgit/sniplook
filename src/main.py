from src.config import get_database_path
from src.db.sqlite import SQLiteDatabase
from src.models.base_snippet import SnippetCreate, SnippetInDB
from src.search.diff_search import match_by_closeness, match_by_ratio

db_connection = SQLiteDatabase(db_path=get_database_path())


def create_snippet_tags(snippet_content: str) -> list[str]:
    return ["command"]


def add_snippet(snippet_content: str) -> SnippetInDB:
    tags = create_snippet_tags(snippet_content=snippet_content)
    db_connection.create_snippet(SnippetCreate(content=snippet_content, tags=tags))


def search_snippet(search_query: str):
    search_result = set()
    fts_search_result = db_connection.search_snippets(query=search_query)

    id_returned: list[int] = []

    for hit in fts_search_result:
        search_result.add(hit.content)
        id_returned.append(hit.id)

    remaining_rows = db_connection._get_data_for_remaining_id(
        [hit.id for hit in fts_search_result]
    )

    if remaining_rows:
        for row in remaining_rows:
            if match_by_closeness(search_query, row.content):
                search_result.add(row.content)
            elif match_by_ratio(search_query, row.content):
                search_result.add(row.content)

    return search_result
