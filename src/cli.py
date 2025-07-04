import argparse
import json
import logging
import sys

from src.format import colored
from src.main import add_snippet, search_snippet

# Create the logger after configuring logging
logger = logging.getLogger(__name__)


def set_logging_level(verbose_count: int):
    log_level = logging.WARNING  # Default level
    if verbose_count == 1:
        log_level = logging.INFO
    elif verbose_count == 2:
        log_level = logging.DEBUG
    elif verbose_count >= 3:
        log_level = logging.DEBUG

    # Configure logging at the module level
    logging.basicConfig(
        level=log_level, format="[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
    )


def handle_default(args):
    """Handle the default search command"""
    set_logging_level(args.verbose)

    value = input("search: ")

    resp = search_snippet(value)

    print("---")
    for hit in resp:
        print(colored(hit))

    if args.output_file:
        try:
            json.dump(resp, args.output_file, indent=4)
            print(f"Release data has been written to {args.output_file.name}")
        except Exception as e:
            print(f"Error writing to {args.output_file.name}: {e}")
    else:
        logger.info("No output file specified. Skipping file write.")


def handle_add(args):
    """Reads input until first Ctrl+Z (Windows) / Ctrl+D (Unix), even on the same line."""
    set_logging_level(args.verbose)
    print("-")  # Prompt for input
    # # Read all input at once, but detect EOF immediately
    try:
        input_text = sys.stdin.read()  # Will stop at first EOF (Ctrl+Z/D)
    except KeyboardInterrupt:
        print("\nInput cancelled.")
        return
    
    lines = input_text.splitlines()
    value = "\n".join(lines)
    
    if not value:
        return  # Skip if empty
    
    add_snippet(value)



def entry_point():
    parser = argparse.ArgumentParser(
        description="Store and Search snippet  in Database."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity of logs. Use multiple times for more verbosity.",
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command")

    # Default command (search)
    default_parser = subparsers.add_parser("search", help="Default search command")
    default_parser.add_argument(
        "--output-file",
        type=argparse.FileType("w"),
        help="File to dump release data as JSON",
        default=None,
    )
    default_parser.set_defaults(func=handle_default)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add an entry to the database")
    add_parser.set_defaults(func=handle_add)

    args = parser.parse_args()

    # If no command provided, default to search
    if not hasattr(args, "func"):
        args.func = handle_default
        args.output_file = None

    args.func(args)


if __name__ == "__main__":
    entry_point()
