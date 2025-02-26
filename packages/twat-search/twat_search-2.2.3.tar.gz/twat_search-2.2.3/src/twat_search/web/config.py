# this_file: src/twat_search/web/config.py

"""
Configuration management for the twat_search.web module.

This module provides classes for loading and accessing configuration
settings for the web search functionality.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, ClassVar

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Default configuration dictionary
DEFAULT_CONFIG: dict[str, Any] = {
    "engines": {
        # Brave Search
        "brave": {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "country": "US",
                "language": "en-US",
                "safe_search": True,
            },
        },
        "brave_news": {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "country": "US",
                "language": "en-US",
                "safe_search": True,
            },
        },
        # SerpAPI (Google)
        "serpapi": {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "country": "us",
                "language": "en",
                "safe_search": True,
            },
        },
        # Tavily Search
        "tavily": {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "search_depth": "basic",
                "include_domains": None,
                "exclude_domains": None,
                "return_rank": True,
                "max_tokens": None,
                "api_version": "2023-11-08",
            },
        },
        # Perplexity AI
        "pplx": {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "model": "search",
            },
        },
        # You.com Search
        "you": {
            "enabled": True,
            "api_key": None,
            "default_params": {},
        },
        "you_news": {
            "enabled": True,
            "api_key": None,
            "default_params": {},
        },
        # Critique Labs
        "critique": {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "source_whitelist": None,
                "source_blacklist": None,
                "additional_params": None,
                "image_url": None,
            },
        },
        # DuckDuckGo
        "duckduckgo": {
            "enabled": True,
            "api_key": None,  # DuckDuckGo doesn't require an API key
            "default_params": {"timeout": 10},
        },
        # Bing Scraper
        "bing_scraper": {
            "enabled": True,
            "api_key": None,  # No API key required, it's a scraper
            "default_params": {"num_pages": 1, "delay": 0.5},
        },
        # HasData Google
        "hasdata_google": {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "device_type": "desktop",
            },
        },
        "hasdata_google_light": {
            "enabled": True,
            "api_key": None,
            "default_params": {},
        },
    }
}


# Engine-specific configuration model
class EngineConfig(BaseModel):
    """Configuration for a single search engine."""

    enabled: bool = True
    api_key: str | None = None
    default_params: dict[str, Any] = Field(default_factory=dict)


# Import standardize_engine_name only after defining all classes to avoid circular imports
from .engines import standardize_engine_name


# Main configuration model
class Config(BaseModel):
    """Main configuration model for the web search module."""

    engines: dict[str, EngineConfig] = Field(default_factory=dict)
    config_path: ClassVar[str | None] = None

    @classmethod
    def get_config_path(cls) -> Path:
        """Get the path to the configuration file.

        Returns:
            Path to the configuration file
        """
        if cls.config_path:
            return Path(cls.config_path)

        # Find the configuration directory
        config_dir = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        config_file = config_dir / "twat_search" / "config.json"
        return config_file

    def __init__(self, **data: Any) -> None:
        """Initialize configuration by loading defaults and user settings.

        Args:
            **data: Additional configuration parameters
        """
        # Start with default configuration
        config_data = DEFAULT_CONFIG.copy()

        # Load configuration from file if it exists
        config_file = self.get_config_path()
        if config_file.exists():
            try:
                with open(config_file, encoding="utf-8") as f:
                    user_config = json.load(f)
                    # Deep merge user configuration with defaults
                    self._merge_config(config_data, user_config)
            except Exception as e:
                logger.warning(f"Failed to load configuration from {config_file}: {e}")

        # Apply environment variable overrides
        self._apply_env_overrides(config_data)

        # Apply any directly provided data
        self._merge_config(config_data, data)

        # Standardize engine names
        engines_data = config_data.get("engines", {})
        standardized_engines = {}
        for engine_name, engine_config in engines_data.items():
            std_name = standardize_engine_name(engine_name)
            standardized_engines[std_name] = engine_config
        config_data["engines"] = standardized_engines

        # Initialize the model
        super().__init__(**config_data)

    def _apply_env_overrides(self, config_data: dict[str, Any]) -> None:
        """Apply configuration overrides from environment variables.

        Args:
            config_data: Configuration data to update
        """
        engine_settings = config_data.get("engines", {})

        # Look for API keys in environment variables
        for engine_name in engine_settings:
            std_engine_name = standardize_engine_name(engine_name)
            # API key environment variables
            api_key_vars = [
                f"{std_engine_name.upper()}_API_KEY",
                f"TWAT_SEARCH_{std_engine_name.upper()}_API_KEY",
            ]
            for env_var in api_key_vars:
                if env_var in os.environ:
                    if std_engine_name not in engine_settings:
                        engine_settings[std_engine_name] = {}
                    engine_settings[std_engine_name]["api_key"] = os.environ[env_var]
                    engine_settings[std_engine_name]["enabled"] = True
                    break

            # Enabled flag environment variables
            enabled_vars = [
                f"{std_engine_name.upper()}_ENABLED",
                f"TWAT_SEARCH_{std_engine_name.upper()}_ENABLED",
            ]
            for env_var in enabled_vars:
                if env_var in os.environ:
                    if std_engine_name not in engine_settings:
                        engine_settings[std_engine_name] = {}
                    engine_settings[std_engine_name]["enabled"] = os.environ[
                        env_var
                    ].lower() in ("true", "1", "yes", "y")
                    break

            # Default parameters from environment variables
            params_vars = [
                f"{std_engine_name.upper()}_DEFAULT_PARAMS",
                f"TWAT_SEARCH_{std_engine_name.upper()}_DEFAULT_PARAMS",
            ]
            for env_var in params_vars:
                if env_var in os.environ:
                    try:
                        if std_engine_name not in engine_settings:
                            engine_settings[std_engine_name] = {}
                        if "default_params" not in engine_settings[std_engine_name]:
                            engine_settings[std_engine_name]["default_params"] = {}
                        params = json.loads(os.environ[env_var])
                        if isinstance(params, dict):
                            engine_settings[std_engine_name]["default_params"].update(
                                params
                            )
                    except json.JSONDecodeError:
                        logger.warning(
                            f"Failed to parse JSON from environment variable {env_var}"
                        )
                    break

    def _merge_config(self, target: dict[str, Any], source: dict[str, Any]) -> None:
        """Recursively merge source configuration into target.

        Args:
            target: Target configuration to update
            source: Source configuration to merge from
        """
        for key, value in source.items():
            if (
                key in target
                and isinstance(target[key], dict)
                and isinstance(value, dict)
            ):
                self._merge_config(target[key], value)
            else:
                target[key] = value

    def add_engine(
        self,
        engine_name: str,
        enabled: bool = True,
        api_key: str | None = None,
        default_params: dict[str, Any] | None = None,
    ) -> None:
        """Add or update an engine configuration.

        Args:
            engine_name: Name of the engine
            enabled: Whether the engine is enabled
            api_key: API key for the engine (if required)
            default_params: Default parameters for the engine
        """
        std_engine_name = standardize_engine_name(engine_name)
        self.engines[std_engine_name] = EngineConfig(
            enabled=enabled,
            api_key=api_key,
            default_params=default_params or {},
        )
