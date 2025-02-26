#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["anywebsearch"]
# ///
# this_file: src/twat_search/web/engines/anywebsearch.py

"""
AnyWebSearch based search engine implementations.

This module implements multiple search engine integrations using the anywebsearch library.
It provides a unified interface for searching across different search engines:
Google, Bing, Brave, Qwant, and Yandex.

The AnyWebSearchEngine class is the base class for all anywebsearch-based engines, with
specific implementations for each search provider.
"""

import logging
from typing import Any, ClassVar

from pydantic import BaseModel, HttpUrl, ValidationError, field_validator

try:
    from anywebsearch import multi_search, Settings
    from anywebsearch.tools import SearchResult as AnySearchResult
except ImportError:
    # For type checking when anywebsearch is not installed
    class AnySearchResult:  # type: ignore
        """Dummy class for type checking when anywebsearch is not installed."""

        def __init__(self, title: str, description: str, url: str):
            """
            Initialize a dummy AnySearchResult for type checking.

            Args:
                title: Title of the result
                description: Description of the result
                url: URL of the result
            """
            self.title = title
            self.description = description
            self.url = url

    class Settings:  # type: ignore
        """Dummy class for type checking when anywebsearch is not installed."""

        def __init__(
            self,
            language: str = "en",
            num_results: int = 20,
            merge: bool = True,
            engines: list[str] | None = None,
            **kwargs: Any,
        ):
            """
            Initialize a dummy Settings for type checking.

            Args:
                language: Language for the search
                num_results: Number of results to retrieve
                merge: Whether to merge results from different engines
                engines: List of engines to use
                **kwargs: Additional settings like API keys
            """
            self.language = language
            self.num_results = num_results
            self.merge = merge
            self.engines = engines or []
            self.extra = kwargs

    def multi_search(query: str, settings: Settings) -> list[AnySearchResult]:  # type: ignore
        """Dummy function for type checking when anywebsearch is not installed."""
        return []


from twat_search.web.config import EngineConfig
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine

logger = logging.getLogger(__name__)


class AnyWebSearchResult(BaseModel):
    """
    Pydantic model for a single AnyWebSearch search result.

    This model is used to validate the response from the AnyWebSearch.
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


class AnyWebSearchEngine(SearchEngine):
    """
    Base implementation for all anywebsearch-based search engines.

    This class provides common functionality for all anywebsearch-based engines,
    including result conversion and error handling.

    Attributes:
        name: Must be overridden by subclasses
        engine_name: Name of the engine in anywebsearch (must be overridden)
        env_api_key_names: API key names for engines that need them
    """

    name = ""  # Must be overridden by subclasses
    engine_name = ""  # Must be overridden - the name used by anywebsearch library
    env_api_key_names: ClassVar[list[str]] = []  # Override as needed

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
        Initialize the AnyWebSearch engine.

        Args:
            config: Engine configuration
            num_results: Number of results to return
            country: Country code for results
            language: Language code for results
            safe_search: Whether to enable safe search (not used by all engines)
            time_frame: Time frame for results (not used by all engines)
            **kwargs: Additional engine-specific parameters
        """
        super().__init__(config, **kwargs)
        self.max_results: int = num_results or self.config.default_params.get(
            "max_results", 5
        )
        self.language: str = language or self.config.default_params.get(
            "language", "en"
        )

        # Unused parameters that might be needed for specific engines
        self.unused_params: dict[str, Any] = {}
        if country:
            self.unused_params["country"] = country
        if safe_search is not None:
            self.unused_params["safe_search"] = safe_search
        if time_frame:
            self.unused_params["time_frame"] = time_frame

        # Extract any API keys or additional settings
        self.brave_key: str | None = kwargs.get(
            "brave_key"
        ) or self.config.default_params.get("brave_key", None)

        self.ya_key: str | None = kwargs.get(
            "ya_key"
        ) or self.config.default_params.get("ya_key", None)

        self.ya_fldid: str | None = kwargs.get(
            "ya_fldid"
        ) or self.config.default_params.get("ya_fldid", None)

    def _convert_result(self, result: AnySearchResult) -> SearchResult | None:
        """
        Convert a raw result from AnySearchResult into a SearchResult.

        This method validates the raw result using the AnyWebSearchResult model
        and converts it to the standard SearchResult format if valid.

        Args:
            result: Raw result object from AnyWebSearch

        Returns:
            SearchResult object or None if validation fails
        """
        if not result:
            logger.warning(f"Empty result received from {self.name}")
            return None

        try:
            # Validate result fields
            validated = AnyWebSearchResult(
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

    def _create_settings(self) -> Settings:
        """
        Create anywebsearch Settings object with the appropriate configuration.

        Returns:
            Settings object for anywebsearch
        """
        settings_kwargs = {}

        # Add API keys if needed
        if self.engine_name == "brave" and self.brave_key:
            settings_kwargs["brave_key"] = self.brave_key

        if self.engine_name == "yandex" and self.ya_key and self.ya_fldid:
            settings_kwargs["ya_key"] = self.ya_key
            settings_kwargs["ya_fldid"] = self.ya_fldid

        # Create settings
        return Settings(
            language=self.language,
            num_results=self.max_results,
            merge=True,  # Always merge for single engine
            engines=[self.engine_name],
            **settings_kwargs,
        )


@register_engine
class GoogleAnyWebSearchEngine(AnyWebSearchEngine):
    """
    Implementation of Google search using anywebsearch library.

    Attributes:
        name: The name of the search engine ("google-anyws")
        engine_name: Name used in anywebsearch library ("google")
    """

    name = "google-anyws"
    engine_name = "google"

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using Google via anywebsearch.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        if not query:
            raise EngineError(self.name, "Search query cannot be empty")

        logger.info(f"Searching Google (anywebsearch) with query: '{query}'")
        logger.debug(f"Using max_results={self.max_results}, language={self.language}")

        try:
            # Create settings and run search
            settings = self._create_settings()

            # Run the search
            raw_results = multi_search(query=query, settings=settings)

            if not raw_results:
                logger.info("No results returned from Google (anywebsearch)")
                return []

            # If merged, results are returned as a single list
            if isinstance(raw_results[0], AnySearchResult):
                raw_results_list = raw_results
            else:
                # If not merged, results are returned as a list of lists
                raw_results_list = raw_results[0]

            logger.debug(
                f"Received {len(raw_results_list)} raw results from Google (anywebsearch)"
            )

            # Convert results
            results: list[SearchResult] = [
                search_result
                for search_result in (
                    self._convert_result(result) for result in raw_results_list
                )
                if search_result is not None
            ]

            logger.info(
                f"Returning {len(results)} validated results from Google (anywebsearch)"
            )
            return results

        except Exception as exc:
            error_msg = f"Error during Google (anywebsearch) search: {exc}"
            logger.error(error_msg)
            raise EngineError(self.name, error_msg) from exc


@register_engine
class BingAnyWebSearchEngine(AnyWebSearchEngine):
    """
    Implementation of Bing (DuckDuckGo) search using anywebsearch library.

    Attributes:
        name: The name of the search engine ("bing-anyws")
        engine_name: Name used in anywebsearch library ("duck")
    """

    name = "bing-anyws"
    engine_name = "duck"  # anywebsearch uses DuckDuckGo API which uses Bing backend

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using Bing (via DuckDuckGo) via anywebsearch.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        if not query:
            raise EngineError(self.name, "Search query cannot be empty")

        logger.info(f"Searching Bing (anywebsearch) with query: '{query}'")
        logger.debug(f"Using max_results={self.max_results}, language={self.language}")

        try:
            # Create settings and run search
            settings = self._create_settings()

            # Run the search
            raw_results = multi_search(query=query, settings=settings)

            if not raw_results:
                logger.info("No results returned from Bing (anywebsearch)")
                return []

            # If merged, results are returned as a single list
            if isinstance(raw_results[0], AnySearchResult):
                raw_results_list = raw_results
            else:
                # If not merged, results are returned as a list of lists
                raw_results_list = raw_results[0]

            logger.debug(
                f"Received {len(raw_results_list)} raw results from Bing (anywebsearch)"
            )

            # Convert results
            results: list[SearchResult] = [
                search_result
                for search_result in (
                    self._convert_result(result) for result in raw_results_list
                )
                if search_result is not None
            ]

            logger.info(
                f"Returning {len(results)} validated results from Bing (anywebsearch)"
            )
            return results

        except Exception as exc:
            error_msg = f"Error during Bing (anywebsearch) search: {exc}"
            logger.error(error_msg)
            raise EngineError(self.name, error_msg) from exc


@register_engine
class BraveAnyWebSearchEngine(AnyWebSearchEngine):
    """
    Implementation of Brave search using anywebsearch library.

    Attributes:
        name: The name of the search engine ("brave-anyws")
        engine_name: Name used in anywebsearch library ("brave")
        env_api_key_names: API key environment variable names
    """

    name = "brave-anyws"
    engine_name = "brave"
    env_api_key_names: ClassVar[list[str]] = ["BRAVE_API_KEY", "BRAVE_KEY"]

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using Brave via anywebsearch.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        if not query:
            raise EngineError(self.name, "Search query cannot be empty")

        if not self.brave_key:
            raise EngineError(self.name, "Brave API key is required for Brave search")

        logger.info(f"Searching Brave (anywebsearch) with query: '{query}'")
        logger.debug(f"Using max_results={self.max_results}, language={self.language}")

        try:
            # Create settings and run search
            settings = self._create_settings()

            # Run the search
            raw_results = multi_search(query=query, settings=settings)

            if not raw_results:
                logger.info("No results returned from Brave (anywebsearch)")
                return []

            # If merged, results are returned as a single list
            if isinstance(raw_results[0], AnySearchResult):
                raw_results_list = raw_results
            else:
                # If not merged, results are returned as a list of lists
                raw_results_list = raw_results[0]

            logger.debug(
                f"Received {len(raw_results_list)} raw results from Brave (anywebsearch)"
            )

            # Convert results
            results: list[SearchResult] = [
                search_result
                for search_result in (
                    self._convert_result(result) for result in raw_results_list
                )
                if search_result is not None
            ]

            logger.info(
                f"Returning {len(results)} validated results from Brave (anywebsearch)"
            )
            return results

        except Exception as exc:
            error_msg = f"Error during Brave (anywebsearch) search: {exc}"
            logger.error(error_msg)
            raise EngineError(self.name, error_msg) from exc


@register_engine
class QwantAnyWebSearchEngine(AnyWebSearchEngine):
    """
    Implementation of Qwant search using anywebsearch library.

    Attributes:
        name: The name of the search engine ("qwant-anyws")
        engine_name: Name used in anywebsearch library ("qwant")
    """

    name = "qwant-anyws"
    engine_name = "qwant"

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using Qwant via anywebsearch.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        if not query:
            raise EngineError(self.name, "Search query cannot be empty")

        logger.info(f"Searching Qwant (anywebsearch) with query: '{query}'")
        logger.debug(f"Using max_results={self.max_results}, language={self.language}")

        try:
            # Create settings and run search
            settings = self._create_settings()

            # Run the search
            raw_results = multi_search(query=query, settings=settings)

            if not raw_results:
                logger.info("No results returned from Qwant (anywebsearch)")
                return []

            # If merged, results are returned as a single list
            if isinstance(raw_results[0], AnySearchResult):
                raw_results_list = raw_results
            else:
                # If not merged, results are returned as a list of lists
                raw_results_list = raw_results[0]

            logger.debug(
                f"Received {len(raw_results_list)} raw results from Qwant (anywebsearch)"
            )

            # Convert results
            results: list[SearchResult] = [
                search_result
                for search_result in (
                    self._convert_result(result) for result in raw_results_list
                )
                if search_result is not None
            ]

            logger.info(
                f"Returning {len(results)} validated results from Qwant (anywebsearch)"
            )
            return results

        except Exception as exc:
            error_msg = f"Error during Qwant (anywebsearch) search: {exc}"
            logger.error(error_msg)
            raise EngineError(self.name, error_msg) from exc


@register_engine
class YandexAnyWebSearchEngine(AnyWebSearchEngine):
    """
    Implementation of Yandex search using anywebsearch library.

    Attributes:
        name: The name of the search engine ("yandex-anyws")
        engine_name: Name used in anywebsearch library ("yandex")
        env_api_key_names: API key environment variable names
    """

    name = "yandex-anyws"
    engine_name = "yandex"
    env_api_key_names: ClassVar[list[str]] = ["YANDEX_API_KEY", "YA_KEY"]

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using Yandex via anywebsearch.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        if not query:
            raise EngineError(self.name, "Search query cannot be empty")

        if not self.ya_key or not self.ya_fldid:
            raise EngineError(
                self.name, "Yandex API key and folder ID are required for Yandex search"
            )

        logger.info(f"Searching Yandex (anywebsearch) with query: '{query}'")
        logger.debug(f"Using max_results={self.max_results}, language={self.language}")

        try:
            # Create settings and run search
            settings = self._create_settings()

            # Run the search
            raw_results = multi_search(query=query, settings=settings)

            if not raw_results:
                logger.info("No results returned from Yandex (anywebsearch)")
                return []

            # If merged, results are returned as a single list
            if isinstance(raw_results[0], AnySearchResult):
                raw_results_list = raw_results
            else:
                # If not merged, results are returned as a list of lists
                raw_results_list = raw_results[0]

            logger.debug(
                f"Received {len(raw_results_list)} raw results from Yandex (anywebsearch)"
            )

            # Convert results
            results: list[SearchResult] = [
                search_result
                for search_result in (
                    self._convert_result(result) for result in raw_results_list
                )
                if search_result is not None
            ]

            logger.info(
                f"Returning {len(results)} validated results from Yandex (anywebsearch)"
            )
            return results

        except Exception as exc:
            error_msg = f"Error during Yandex (anywebsearch) search: {exc}"
            logger.error(error_msg)
            raise EngineError(self.name, error_msg) from exc


# Convenience functions for each engine
async def google_anyws(
    query: str,
    num_results: int = 5,
    language: str = "en",
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search using Google via anywebsearch.

    Args:
        query: The search query
        num_results: Number of results to return
        language: Language code for results
        **kwargs: Additional parameters to pass to the search engine

    Returns:
        List of search results

    Raises:
        EngineError: If the search fails
    """
    from twat_search.web.api import search

    return await search(
        query,
        engines=["google-anyws"],
        num_results=num_results,
        language=language,
        **kwargs,
    )


async def bing_anyws(
    query: str,
    num_results: int = 5,
    language: str = "en",
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search using Bing (DuckDuckGo) via anywebsearch.

    Args:
        query: The search query
        num_results: Number of results to return
        language: Language code for results
        **kwargs: Additional parameters to pass to the search engine

    Returns:
        List of search results

    Raises:
        EngineError: If the search fails
    """
    from twat_search.web.api import search

    return await search(
        query,
        engines=["bing-anyws"],
        num_results=num_results,
        language=language,
        **kwargs,
    )


async def brave_anyws(
    query: str,
    num_results: int = 5,
    language: str = "en",
    brave_key: str | None = None,
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search using Brave via anywebsearch.

    Args:
        query: The search query
        num_results: Number of results to return
        language: Language code for results
        brave_key: Brave API key
        **kwargs: Additional parameters to pass to the search engine

    Returns:
        List of search results

    Raises:
        EngineError: If the search fails
    """
    from twat_search.web.api import search

    return await search(
        query,
        engines=["brave-anyws"],
        num_results=num_results,
        language=language,
        brave_anyws_brave_key=brave_key,
        **kwargs,
    )


async def qwant_anyws(
    query: str,
    num_results: int = 5,
    language: str = "en",
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search using Qwant via anywebsearch.

    Args:
        query: The search query
        num_results: Number of results to return
        language: Language code for results
        **kwargs: Additional parameters to pass to the search engine

    Returns:
        List of search results

    Raises:
        EngineError: If the search fails
    """
    from twat_search.web.api import search

    return await search(
        query,
        engines=["qwant-anyws"],
        num_results=num_results,
        language=language,
        **kwargs,
    )


async def yandex_anyws(
    query: str,
    num_results: int = 5,
    language: str = "en",
    ya_key: str | None = None,
    ya_fldid: str | None = None,
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search using Yandex via anywebsearch.

    Args:
        query: The search query
        num_results: Number of results to return
        language: Language code for results
        ya_key: Yandex API key
        ya_fldid: Yandex folder ID
        **kwargs: Additional parameters to pass to the search engine

    Returns:
        List of search results

    Raises:
        EngineError: If the search fails
    """
    from twat_search.web.api import search

    return await search(
        query,
        engines=["yandex-anyws"],
        num_results=num_results,
        language=language,
        yandex_anyws_ya_key=ya_key,
        yandex_anyws_ya_fldid=ya_fldid,
        **kwargs,
    )
