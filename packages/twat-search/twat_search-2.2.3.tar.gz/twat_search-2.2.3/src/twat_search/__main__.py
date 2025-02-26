#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["fire>=0.5.0", "rich>=13.6.0"]
# ///
# this_file: src/twat_search/__main__.py

"""
Main entry point for the Twat Search CLI.
"""

import logging
from typing import Any, TypeVar

import fire  # type: ignore
from rich.console import Console
from rich.logging import RichHandler

# Set up logging with rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)
console = Console()

# Define types for the CLI components
SearchCLIType = TypeVar("SearchCLIType")


class TwatSearchCLI:
    """Twat Search Command Line Interface."""

    def __init__(self) -> None:
        """Initialize the Twat Search CLI."""
        # Try to import the web CLI module
        try:
            from twat_search.web import cli as web_cli

            self.web: Any = web_cli.SearchCLI()
        except (ImportError, AttributeError) as e:
            # Create a placeholder if the web CLI is not available
            logger.error(f"Web CLI not available: {e!s}")
            logger.error("Make sure twat_search.web.cli is properly installed.")
            self.web = self._cli_error

    def _cli_error(self, *args: Any, **kwargs: Any) -> int:  # noqa: ARG002
        """Placeholder function when web CLI is not available.

        Args are ignored but necessary to match any possible call signature.
        """
        console.print(
            "[bold red]Web CLI not available. Make sure twat_search.web.cli is properly installed.[/bold red]"
        )
        return 1

    def version(self) -> str:
        """Display the version of the Twat Search tool."""
        try:
            from twat_search.__version__ import version

            return f"Twat Search version {version}"
        except ImportError:
            return "Twat Search (version not available)"


def main() -> None:
    from rich.ansi import AnsiDecoder
    from rich.console import Console, Group
    from rich.theme import Theme
    from rich.traceback import install

    install(show_locals=True)
    ansi_decoder = AnsiDecoder()
    console = Console(theme=Theme({"prompt": "cyan", "question": "bold cyan"}))

    def display(lines, out):
        console.print(Group(*map(ansi_decoder.decode_line, lines)))

    fire.core.Display = display

    fire.Fire(TwatSearchCLI, name="twat-search")


if __name__ == "__main__":
    main()
