"""Shared Pytest options and fixtures for environment-aware API testing."""

import pytest

from client.api_client import ApiClient


ENVIRONMENT_URLS = {
    "prod": "https://jsonplaceholder.typicode.com",
    "staging": "https://jsonplaceholder.typicode.com",
    "dev": "https://jsonplaceholder.typicode.com",
}


def pytest_addoption(parser: pytest.Parser) -> None:
    """Goal: register the supported API environment command-line option.

    Assertion: `--env` defaults to prod and accepts prod, staging, or dev.
    SDET Rationale: the same suite can target deployment tiers without source changes.
    """
    parser.addoption(
        "--env",
        action="store",
        default="prod",
        choices=sorted(ENVIRONMENT_URLS),
        help="Target API environment: prod, staging, or dev.",
    )


@pytest.fixture(scope="session")
def base_url(request: pytest.FixtureRequest) -> str:
    """Goal: resolve the base URL selected by the `--env` option.

    Assertion: the URL belongs to the explicitly supported environment map.
    SDET Rationale: centralized resolution avoids accidental cross-environment tests.
    """
    environment = request.config.getoption("--env")
    return ENVIRONMENT_URLS[environment]


@pytest.fixture(scope="session")
def api_client(base_url: str) -> ApiClient:
    """Goal: provide one environment-configured client for the test session.

    Assertion: all tests use the selected base URL and teardown closes the session.
    SDET Rationale: fixture-scoped reuse preserves connection pooling and test speed.
    """
    client = ApiClient(base_url=base_url)
    yield client
    client.close()


@pytest.fixture
def post_payload() -> dict[str, object]:
    """Goal: provide a valid POST `/posts` payload for CRUD coverage.

    Assertion: the payload contains the API's required user, title, and body fields.
    SDET Rationale: a stable fixture isolates request construction from response assertions.
    """
    return {
        "userId": 1,
        "title": "SDET API test post",
        "body": "Created during the contract test suite.",
    }
