#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["googlesearch-python"]
# ///
# this_file: src/twat_search/web/engines/google_scraper.py

"""
Google Scraper search engine implementation.

This module implements the Google search integration using the googlesearch-python library.
It provides a web scraping approach to search Google without requiring an API key.

The GoogleScraperEngine class handles all interactions with the googlesearch-python
library, providing robust error handling, result validation, and conversion to
the standard SearchResult format used throughout the package.
"""

import logging
from typing import Any, ClassVar, cast

from pydantic import BaseModel, HttpUrl, ValidationError, field_validator

try:
    from googlesearch import search as google_search
    from googlesearch import SearchResult as GoogleSearchResult
except ImportError:
    # For type checking when googlesearch-python is not installed
    class GoogleSearchResult:  # type: ignore
        """Dummy class for type checking when googlesearch-python is not installed."""

        def __init__(self, url: str, title: str, description: str):
            """
            Initialize a dummy GoogleSearchResult for type checking.

            Args:
                url: The URL of the search result
                title: The title of the search result
                description: The description of the search result
            """
            self.url = url
            self.title = title
            self.description = description

    def google_search(*args, **kwargs):  # type: ignore
        """Dummy function for type checking when googlesearch-python is not installed."""
        return []


from twat_search.web.config import EngineConfig
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine

logger = logging.getLogger(__name__)


class GoogleScraperResult(BaseModel):
    """
    Pydantic model for a single Google Scraper search result.

    This model is used to validate the response from the Google Scraper.
    It ensures that each result has the required fields and proper types
    before being converted to the standard SearchResult format.

    Attributes:
        title: The title of the search result
        url: The URL of the search result, validated as a proper HTTP URL
        description: Description/snippet of the search result
    """

    title: str
    url: HttpUrl
    description: str = ""

    @field_validator("title", "description")
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        """Ensure string fields are not None and convert to empty string if None."""
        return v or ""


@register_engine
class GoogleScraperEngine(SearchEngine):
    """
    Implementation of Google search using googlesearch-python library.

    This engine scrapes Google search results without requiring an API key.
    It provides a way to search Google using web scraping techniques, with
    configurable parameters like language, region, and safe search.

    Attributes:
        name: The name of the search engine ("google-scraper")
        env_api_key_names: Empty list since no API key is needed
    """

    name = "google-scraper"
    env_api_key_names: ClassVar[list[str]] = []  # No API key needed

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | str | None = True,
        time_frame: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize Google Scraper Search engine.

        Args:
            config: Engine configuration
            num_results: Number of results to return
            country: Country code for results (used as region parameter)
            language: Language code for results
            safe_search: Whether to enable safe search
            time_frame: Time frame for results (not used by Google Scraper, kept for interface consistency)
            **kwargs: Additional Google Scraper-specific parameters including:
                sleep_interval: Sleep interval between requests in seconds
                ssl_verify: Whether to verify SSL certificates
                proxy: Proxy to use for requests
                unique: Whether to return only unique results
        """
        super().__init__(config, **kwargs)
        self.max_results: int = num_results or self.config.default_params.get(
            "max_results", 5
        )
        self.language: str = language or self.config.default_params.get(
            "language", "en"
        )
        self.region: str | None = country or self.config.default_params.get(
            "region", None
        )
        self.safe: str | None = (
            ("active" if safe_search else None)
            if safe_search is not None
            else self.config.default_params.get("safe", "active")
        )

        self.sleep_interval: float = kwargs.get(
            "sleep_interval"
        ) or self.config.default_params.get("sleep_interval", 0.0)
        self.ssl_verify: bool | None = kwargs.get(
            "ssl_verify"
        ) or self.config.default_params.get("ssl_verify", None)
        self.proxy: str | None = kwargs.get("proxy") or self.config.default_params.get(
            "proxy", None
        )
        self.unique: bool = kwargs.get("unique") or self.config.default_params.get(
            "unique", True
        )

        # Log any unused parameters for clarity
        unused_params: list[str] = []
        if time_frame:
            unused_params.append(f"time_frame='{time_frame}'")
        if unused_params:
            logger.debug(
                f"Parameters {', '.join(unused_params)} set but not used by Google Scraper"
            )

    def _convert_result(self, result: GoogleSearchResult) -> SearchResult | None:
        """
        Convert a raw result from GoogleSearchResult into a SearchResult.

        This method validates the raw result using the GoogleScraperResult model
        and converts it to the standard SearchResult format if valid.

        Args:
            result: Raw result object from the Google search

        Returns:
            SearchResult object or None if validation fails
        """
        if not result:
            logger.warning("Empty result received from Google Scraper")
            return None

        try:
            # Validate result fields
            validated = GoogleScraperResult(
                title=result.title,
                url=result.url,
                description=result.description
                if hasattr(result, "description")
                else "",
            )

            # Create and return the SearchResult
            return SearchResult(
                title=validated.title,
                url=validated.url,
                snippet=validated.description,
                source=self.name,
                raw={
                    "title": result.title,
                    "url": str(result.url),
                    "description": result.description
                    if hasattr(result, "description")
                    else "",
                },
            )
        except ValidationError as exc:
            logger.warning(f"Validation error for result: {exc}")
            return None
        except Exception as exc:
            logger.warning(f"Unexpected error converting result: {exc}")
            return None

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Google Scraper.

        This method uses the googlesearch-python library, performs the search,
        and converts the results to the standard SearchResult format.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails due to invalid input, network issues,
                         parsing errors, or other exceptions
        """
        if not query:
            raise EngineError(self.name, "Search query cannot be empty")

        logger.info(f"Searching Google with query: '{query}'")
        logger.debug(
            f"Using max_results={self.max_results}, language={self.language}, "
            f"region={self.region}, safe={self.safe}, sleep_interval={self.sleep_interval}, "
            f"ssl_verify={self.ssl_verify}, proxy={self.proxy}, unique={self.unique}"
        )

        try:
            # Perform search using the googlesearch-python library
            raw_results = list(
                google_search(
                    query,
                    num_results=self.max_results,
                    lang=self.language,
                    region=self.region,
                    safe=self.safe,
                    sleep_interval=self.sleep_interval,
                    ssl_verify=self.ssl_verify,
                    proxy=self.proxy,
                    unique=self.unique,
                    advanced=True,  # Always use advanced to get titles and descriptions
                )
            )

            if not raw_results:
                logger.info("No results returned from Google Scraper")
                return []

            logger.debug(f"Received {len(raw_results)} raw results from Google Scraper")

        except ValueError as exc:
            error_msg = f"Invalid input for Google search: {exc}"
            logger.error(error_msg)
            raise EngineError(self.name, error_msg) from exc
        except ConnectionError as exc:
            error_msg = f"Network error connecting to Google: {exc}"
            logger.error(error_msg)
            raise EngineError(self.name, error_msg) from exc
        except RuntimeError as exc:
            error_msg = f"Error parsing Google search results: {exc}"
            logger.error(error_msg)
            raise EngineError(self.name, error_msg) from exc
        except Exception as exc:
            error_msg = f"Unexpected error during Google search: {exc}"
            logger.error(error_msg)
            raise EngineError(self.name, error_msg) from exc

        # Convert and filter results in a single comprehension
        results: list[SearchResult] = [
            search_result
            for search_result in (
                self._convert_result(cast(GoogleSearchResult, result))
                for result in raw_results
            )
            if search_result is not None
        ]

        logger.info(f"Returning {len(results)} validated results from Google Scraper")
        return results


async def google_scraper(
    query: str,
    num_results: int = 5,
    language: str = "en",
    country: str | None = None,
    safe_search: bool = True,
    sleep_interval: float = 0.0,
    ssl_verify: bool | None = None,
    proxy: str | None = None,
    unique: bool = True,
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search using Google Scraper.

    This is a convenience function that calls the main search API with
    the Google Scraper engine.

    Args:
        query: The search query
        num_results: Number of results to return
        language: Language code for results
        country: Country code for results (used as region parameter)
        safe_search: Whether to enable safe search
        sleep_interval: Sleep interval between requests in seconds
        ssl_verify: Whether to verify SSL certificates
        proxy: Proxy to use for requests
        unique: Whether to return only unique results
        **kwargs: Additional parameters to pass to the search engine

    Returns:
        List of search results

    Raises:
        EngineError: If the search fails
    """
    from twat_search.web.api import search

    return await search(
        query,
        engines=["google-scraper"],
        num_results=num_results,
        language=language,
        country=country,
        safe_search=safe_search,
        google_scraper_sleep_interval=sleep_interval,
        google_scraper_ssl_verify=ssl_verify,
        google_scraper_proxy=proxy,
        google_scraper_unique=unique,
        **kwargs,
    )
