"""Centralized environment settings used by the API client and test fixtures."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Expose configurable API connection values with production-safe defaults."""

    base_url: str = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")
    timeout: float = float(os.getenv("API_TIMEOUT", "10"))
    environment: str = os.getenv("API_ENVIRONMENT", "prod")


settings = Settings()
