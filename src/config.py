import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def get_database_path() -> Path:
    """
    It returns the path of database being used to store the snippets.

    Arguments: None

    Returns:
        Path: Path of the database file.
    """

    home_dir: Path = Path.home()

    # Define the directory path
    db_dir = home_dir / ".sniplook" / "db"

    # Create directory if it doesn't exist
    db_dir.mkdir(parents=True, exist_ok=True)

    # Return the full path to the database file
    return db_dir / "snippets.db"
