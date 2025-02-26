#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["searchit"]
# ///
# this_file: src/twat_search/web/engines/searchit.py

"""
Searchit based search engine implementations.

This module implements multiple search engine integrations using the searchit library.
It provides asynchronous search functionality for Google, Yandex, Qwant, and Bing (via searchit).

The SearchitEngine class is the base class for all searchit-based engines, with
specific implementations for each search provider.
"""

import asyncio
import logging
from typing import Any, ClassVar

from pydantic import BaseModel, HttpUrl, ValidationError, field_validator

try:
    from searchit import (
        GoogleScraper,
        YandexScraper,
        BingScraper,
        QwantScraper,
        ScrapeRequest,
    )
    from searchit.scrapers.scraper import SearchResult as SearchitResult
except ImportError:
    # For type checking when searchit is not installed
    class SearchitResult:  # type: ignore
        """Dummy class for type checking when searchit is not installed."""

        def __init__(self, rank: int, url: str, title: str, description: str):
            """
            Initialize a dummy SearchitResult for type checking.

            Args:
                rank: Rank of the result
                url: URL of the result
                title: Title of the result
                description: Description of the result
            """
            self.rank = rank
            self.url = url
            self.title = title
            self.description = description

    class ScrapeRequest:  # type: ignore
        """Dummy class for type checking when searchit is not installed."""

        def __init__(
            self,
            term: str,
            count: int,
            domain: str | None = None,
            sleep: int = 0,
            proxy: str | None = None,
            language: str | None = None,
            geo: str | None = None,
        ):
            """
            Initialize a dummy ScrapeRequest for type checking.

            Args:
                term: Search term
                count: Number of results to retrieve
                domain: Domain for the search
                sleep: Sleep interval between requests
                proxy: Proxy to use
                language: Language for the search
                geo: Geographic location for the search
            """
            self.term = term
            self.count = count
            self.domain = domain
            self.sleep = sleep
            self.proxy = proxy
            self.language = language
            self.geo = geo

    class GoogleScraper:  # type: ignore
        """Dummy class for type checking when searchit is not installed."""

        def __init__(self, max_results_per_page: int = 100):
            """
            Initialize a dummy GoogleScraper for type checking.

            Args:
                max_results_per_page: Maximum results per page
            """
            self.max_results = max_results_per_page

        async def scrape(self, request: ScrapeRequest) -> list[SearchitResult]:
            """
            Dummy scrape method for type checking.

            Args:
                request: Search request

            Returns:
                Empty list (dummy implementation)
            """
            return []

    class YandexScraper:  # type: ignore
        """Dummy class for type checking when searchit is not installed."""

        def __init__(self, max_results_per_page: int = 10):
            """
            Initialize a dummy YandexScraper for type checking.

            Args:
                max_results_per_page: Maximum results per page
            """
            self.max_results = max_results_per_page

        async def scrape(self, request: ScrapeRequest) -> list[SearchitResult]:
            """
            Dummy scrape method for type checking.

            Args:
                request: Search request

            Returns:
                Empty list (dummy implementation)
            """
            return []

    class QwantScraper:  # type: ignore
        """Dummy class for type checking when searchit is not installed."""

        def __init__(self, max_results_per_page: int = 10):
            """
            Initialize a dummy QwantScraper for type checking.

            Args:
                max_results_per_page: Maximum results per page
            """
            self.max_results = max_results_per_page

        async def scrape(self, request: ScrapeRequest) -> list[SearchitResult]:
            """
            Dummy scrape method for type checking.

            Args:
                request: Search request

            Returns:
                Empty list (dummy implementation)
            """
            return []

    class BingScraper:  # type: ignore
        """Dummy class for type checking when searchit is not installed."""

        def __init__(self, max_results_per_page: int = 10):
            """
            Initialize a dummy BingScraper for type checking.

            Args:
                max_results_per_page: Maximum results per page
            """
            self.max_results = max_results_per_page

        async def scrape(self, request: ScrapeRequest) -> list[SearchitResult]:
            """
            Dummy scrape method for type checking.

            Args:
                request: Search request

            Returns:
                Empty list (dummy implementation)
            """
            return []


from twat_search.web.config import EngineConfig
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine

logger = logging.getLogger(__name__)


class SearchitScraperResult(BaseModel):
    """
    Pydantic model for a single Searchit search result.

    This model is used to validate the response from the Searchit scrapers.
    It ensures that each result has the required fields and proper types
    before being converted to the standard SearchResult model.

    Attributes:
        rank: The rank of the search result
        title: The title of the search result
        url: The URL of the search result, validated as a proper HTTP URL
        description: Description/snippet of the search result
    """

    rank: int
    title: str
    url: HttpUrl
    description: str = ""

    @field_validator("title", "description")
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        """Ensure string fields are not None and convert to empty string if None."""
        return v or ""


class SearchitEngine(SearchEngine):
    """
    Base implementation for all searchit-based search engines.

    This class provides common functionality for all searchit-based engines,
    including result conversion and error handling.

    Attributes:
        name: Must be overridden by subclasses
        env_api_key_names: Empty list for scrapers as they don't need API keys
    """

    name = ""  # Must be overridden by subclasses
    env_api_key_names: ClassVar[list[str]] = []  # No API key needed for scrapers

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
        Initialize the Searchit-based search engine.

        Args:
            config: Engine configuration
            num_results: Number of results to return
            country: Country code for results (used as domain parameter)
            language: Language code for results
            safe_search: Whether to enable safe search (not used by Searchit, kept for interface consistency)
            time_frame: Time frame for results (not used by Searchit, kept for interface consistency)
            **kwargs: Additional Searchit-specific parameters including:
                sleep_interval: Sleep interval between requests in seconds
                proxy: Proxy to use for requests
        """
        super().__init__(config, **kwargs)
        self.max_results: int = num_results or self.config.default_params.get(
            "max_results", 5
        )
        self.language: str = language or self.config.default_params.get(
            "language", "en"
        )
        # Some searchit engines use domain, others use geo
        self.domain: str | None = country or self.config.default_params.get(
            "domain", None
        )
        self.geo: str | None = country or self.config.default_params.get("geo", None)

        self.sleep_interval: int = kwargs.get(
            "sleep_interval"
        ) or self.config.default_params.get("sleep_interval", 0)
        self.proxy: str | None = kwargs.get("proxy") or self.config.default_params.get(
            "proxy", None
        )

        # Log any unused parameters for clarity
        unused_params: list[str] = []
        if safe_search is not None:
            unused_params.append(f"safe_search={safe_search}")
        if time_frame:
            unused_params.append(f"time_frame='{time_frame}'")
        if unused_params:
            logger.debug(
                f"Parameters {', '.join(unused_params)} set but not used by {self.name}"
            )

    def _convert_result(self, result: SearchitResult) -> SearchResult | None:
        """
        Convert a raw result from SearchitResult into a SearchResult.

        This method validates the raw result using the SearchitScraperResult model
        and converts it to the standard SearchResult format if valid.

        Args:
            result: Raw result object from the Searchit scraper

        Returns:
            SearchResult object or None if validation fails
        """
        if not result:
            logger.warning(f"Empty result received from {self.name}")
            return None

        try:
            # Validate result fields
            validated = SearchitScraperResult(
                rank=result.rank,
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
                rank=validated.rank,
                raw={
                    "rank": result.rank,
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

    async def _run_scraper(
        self, scraper: Any, request: ScrapeRequest
    ) -> list[SearchitResult]:
        """
        Run a searchit scraper with the given request.

        Args:
            scraper: The searchit scraper instance
            request: The search request

        Returns:
            List of SearchitResult objects
        """
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None, lambda: asyncio.run(scraper.scrape(request))
            )
        except Exception as exc:
            logger.error(f"Error running searchit scraper: {exc}")
            raise EngineError(
                self.name, f"Error running searchit scraper: {exc}"
            ) from exc


@register_engine
class GoogleSearchitEngine(SearchitEngine):
    """
    Implementation of Google search using searchit library.

    Attributes:
        name: The name of the search engine ("google-searchit")
    """

    name = "google-searchit"

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using Google via searchit.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        if not query:
            raise EngineError(self.name, "Search query cannot be empty")

        logger.info(f"Searching Google (searchit) with query: '{query}'")
        logger.debug(
            f"Using max_results={self.max_results}, language={self.language}, "
            f"domain={self.domain}, sleep_interval={self.sleep_interval}, "
            f"proxy={self.proxy}"
        )

        try:
            # Create searchit request and scraper
            request = ScrapeRequest(
                term=query,
                count=self.max_results,
                domain=self.domain,
                sleep=self.sleep_interval,
                proxy=self.proxy,
                language=self.language,
            )

            scraper = GoogleScraper(max_results_per_page=min(100, self.max_results))

            # Run the scraper
            raw_results = await self._run_scraper(scraper, request)

            if not raw_results:
                logger.info("No results returned from Google (searchit)")
                return []

            logger.debug(
                f"Received {len(raw_results)} raw results from Google (searchit)"
            )

            # Convert results
            results: list[SearchResult] = [
                search_result
                for search_result in (
                    self._convert_result(result) for result in raw_results
                )
                if search_result is not None
            ]

            logger.info(
                f"Returning {len(results)} validated results from Google (searchit)"
            )
            return results

        except Exception as exc:
            error_msg = f"Error during Google (searchit) search: {exc}"
            logger.error(error_msg)
            raise EngineError(self.name, error_msg) from exc


@register_engine
class YandexSearchitEngine(SearchitEngine):
    """
    Implementation of Yandex search using searchit library.

    Attributes:
        name: The name of the search engine ("yandex-searchit")
    """

    name = "yandex-searchit"

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using Yandex via searchit.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        if not query:
            raise EngineError(self.name, "Search query cannot be empty")

        logger.info(f"Searching Yandex (searchit) with query: '{query}'")
        logger.debug(
            f"Using max_results={self.max_results}, language={self.language}, "
            f"domain={self.domain}, geo={self.geo}, sleep_interval={self.sleep_interval}, "
            f"proxy={self.proxy}"
        )

        try:
            # Create searchit request and scraper
            request = ScrapeRequest(
                term=query,
                count=self.max_results,
                domain=self.domain,
                sleep=self.sleep_interval,
                proxy=self.proxy,
                geo=self.geo,
            )

            scraper = YandexScraper(max_results_per_page=min(10, self.max_results))

            # Run the scraper
            raw_results = await self._run_scraper(scraper, request)

            if not raw_results:
                logger.info("No results returned from Yandex (searchit)")
                return []

            logger.debug(
                f"Received {len(raw_results)} raw results from Yandex (searchit)"
            )

            # Convert results
            results: list[SearchResult] = [
                search_result
                for search_result in (
                    self._convert_result(result) for result in raw_results
                )
                if search_result is not None
            ]

            logger.info(
                f"Returning {len(results)} validated results from Yandex (searchit)"
            )
            return results

        except Exception as exc:
            error_msg = f"Error during Yandex (searchit) search: {exc}"
            logger.error(error_msg)
            raise EngineError(self.name, error_msg) from exc


@register_engine
class QwantSearchitEngine(SearchitEngine):
    """
    Implementation of Qwant search using searchit library.

    Attributes:
        name: The name of the search engine ("qwant-searchit")
    """

    name = "qwant-searchit"

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using Qwant via searchit.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        if not query:
            raise EngineError(self.name, "Search query cannot be empty")

        logger.info(f"Searching Qwant (searchit) with query: '{query}'")
        logger.debug(
            f"Using max_results={self.max_results}, language={self.language}, "
            f"geo={self.geo}, sleep_interval={self.sleep_interval}, "
            f"proxy={self.proxy}"
        )

        try:
            # Create searchit request and scraper
            request = ScrapeRequest(
                term=query,
                count=self.max_results,
                sleep=self.sleep_interval,
                proxy=self.proxy,
                geo=self.geo,
            )

            scraper = QwantScraper(max_results_per_page=min(10, self.max_results))

            # Run the scraper
            raw_results = await self._run_scraper(scraper, request)

            if not raw_results:
                logger.info("No results returned from Qwant (searchit)")
                return []

            logger.debug(
                f"Received {len(raw_results)} raw results from Qwant (searchit)"
            )

            # Convert results
            results: list[SearchResult] = [
                search_result
                for search_result in (
                    self._convert_result(result) for result in raw_results
                )
                if search_result is not None
            ]

            logger.info(
                f"Returning {len(results)} validated results from Qwant (searchit)"
            )
            return results

        except Exception as exc:
            error_msg = f"Error during Qwant (searchit) search: {exc}"
            logger.error(error_msg)
            raise EngineError(self.name, error_msg) from exc


@register_engine
class BingSearchitEngine(SearchitEngine):
    """
    Implementation of Bing search using searchit library.

    Attributes:
        name: The name of the search engine ("bing-searchit")
    """

    name = "bing-searchit"

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using Bing via searchit.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        if not query:
            raise EngineError(self.name, "Search query cannot be empty")

        logger.info(f"Searching Bing (searchit) with query: '{query}'")
        logger.debug(
            f"Using max_results={self.max_results}, language={self.language}, "
            f"domain={self.domain}, sleep_interval={self.sleep_interval}, "
            f"proxy={self.proxy}"
        )

        try:
            # Create searchit request and scraper
            request = ScrapeRequest(
                term=query,
                count=self.max_results,
                domain=self.domain,
                sleep=self.sleep_interval,
                proxy=self.proxy,
                language=self.language,
            )

            scraper = BingScraper(max_results_per_page=min(30, self.max_results))

            # Run the scraper
            raw_results = await self._run_scraper(scraper, request)

            if not raw_results:
                logger.info("No results returned from Bing (searchit)")
                return []

            logger.debug(
                f"Received {len(raw_results)} raw results from Bing (searchit)"
            )

            # Convert results
            results: list[SearchResult] = [
                search_result
                for search_result in (
                    self._convert_result(result) for result in raw_results
                )
                if search_result is not None
            ]

            logger.info(
                f"Returning {len(results)} validated results from Bing (searchit)"
            )
            return results

        except Exception as exc:
            error_msg = f"Error during Bing (searchit) search: {exc}"
            logger.error(error_msg)
            raise EngineError(self.name, error_msg) from exc


# Convenience functions for each engine
async def google_searchit(
    query: str,
    num_results: int = 5,
    language: str = "en",
    country: str | None = None,
    sleep_interval: int = 0,
    proxy: str | None = None,
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search using Google via searchit.

    Args:
        query: The search query
        num_results: Number of results to return
        language: Language code for results
        country: Country code for results (used as domain parameter)
        sleep_interval: Sleep interval between requests in seconds
        proxy: Proxy to use for requests
        **kwargs: Additional parameters to pass to the search engine

    Returns:
        List of search results

    Raises:
        EngineError: If the search fails
    """
    from twat_search.web.api import search

    return await search(
        query,
        engines=["google-searchit"],
        num_results=num_results,
        language=language,
        country=country,
        google_searchit_sleep_interval=sleep_interval,
        google_searchit_proxy=proxy,
        **kwargs,
    )


async def yandex_searchit(
    query: str,
    num_results: int = 5,
    language: str = "en",
    country: str | None = None,
    sleep_interval: int = 0,
    proxy: str | None = None,
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search using Yandex via searchit.

    Args:
        query: The search query
        num_results: Number of results to return
        language: Language code for results
        country: Country code for results (used as domain and geo parameter)
        sleep_interval: Sleep interval between requests in seconds
        proxy: Proxy to use for requests
        **kwargs: Additional parameters to pass to the search engine

    Returns:
        List of search results

    Raises:
        EngineError: If the search fails
    """
    from twat_search.web.api import search

    return await search(
        query,
        engines=["yandex-searchit"],
        num_results=num_results,
        language=language,
        country=country,
        yandex_searchit_sleep_interval=sleep_interval,
        yandex_searchit_proxy=proxy,
        **kwargs,
    )


async def qwant_searchit(
    query: str,
    num_results: int = 5,
    language: str = "en",
    country: str | None = None,
    sleep_interval: int = 0,
    proxy: str | None = None,
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search using Qwant via searchit.

    Args:
        query: The search query
        num_results: Number of results to return
        language: Language code for results
        country: Country code for results (used as geo parameter)
        sleep_interval: Sleep interval between requests in seconds
        proxy: Proxy to use for requests
        **kwargs: Additional parameters to pass to the search engine

    Returns:
        List of search results

    Raises:
        EngineError: If the search fails
    """
    from twat_search.web.api import search

    return await search(
        query,
        engines=["qwant-searchit"],
        num_results=num_results,
        language=language,
        country=country,
        qwant_searchit_sleep_interval=sleep_interval,
        qwant_searchit_proxy=proxy,
        **kwargs,
    )


async def bing_searchit(
    query: str,
    num_results: int = 5,
    language: str = "en",
    country: str | None = None,
    sleep_interval: int = 0,
    proxy: str | None = None,
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search using Bing via searchit.

    Args:
        query: The search query
        num_results: Number of results to return
        language: Language code for results
        country: Country code for results (used as domain parameter)
        sleep_interval: Sleep interval between requests in seconds
        proxy: Proxy to use for requests
        **kwargs: Additional parameters to pass to the search engine

    Returns:
        List of search results

    Raises:
        EngineError: If the search fails
    """
    from twat_search.web.api import search

    return await search(
        query,
        engines=["bing-searchit"],
        num_results=num_results,
        language=language,
        country=country,
        bing_searchit_sleep_interval=sleep_interval,
        bing_searchit_proxy=proxy,
        **kwargs,
    )
