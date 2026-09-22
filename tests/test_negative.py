"""Negative-path tests for unknown resources and unsupported API routes."""

import pytest

from client.api_client import ApiClient


@pytest.mark.parametrize(
    "path",
    ["/posts/99999", "/comments/99999", "/albums/99999", "/photos/99999", "/todos/99999", "/users/99999"],
)
def test_unknown_resource_id_returns_not_found(api_client: ApiClient, path: str) -> None:
    """Goal: verify unknown IDs return a not-found response for each resource.

    Assertion: every parameterized GET returns HTTP 404.
    SDET Rationale: consistent error semantics prevent false success for missing data.
    """

    response = api_client.get(path)

    api_client.assert_status(response, 404)


def test_unknown_endpoint_returns_not_found(api_client: ApiClient) -> None:
    """Goal: verify an unsupported route is rejected by the API.

    Assertion: GET to an invalid path returns HTTP 404.
    SDET Rationale: route failures must be explicit rather than masquerading as empty data.
    """

    response = api_client.get("/not-a-jsonplaceholder-resource")

    api_client.assert_status(response, 404)
