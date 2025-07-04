import difflib
from difflib import SequenceMatcher


def match_by_ratio(query: str, content_to_match: str) -> float:
    """
    It returns the ratio of matcihng based on similarity.

    Args:
        query (str) : The query to search for.
        content_to_match (str): The content to search against.

    Returns:
        float : The matching ratio.
    """

    matching = SequenceMatcher(
        lambda x: x in " \t" or x in " ", query, content_to_match
    )
    return matching.ratio() >= 0.4


def match_by_closeness(query: str, content_to_match: str) -> bool:
    """
    Returns True if conten have any string which matches the query.

    Args:
        query (str) : The query to search for.
        content_to_match (str): The content to search against.

    Returns:
        float : True if Matches else false.
    """
    close_match = difflib.get_close_matches(query, content_to_match.split(" "), 3, 0.6)
    if len(close_match) >= 1:
        return True
