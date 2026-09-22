"""Parameterized availability checks for every exposed JSONPlaceholder collection."""

import pytest

from client.api_client import ApiClient


RESOURCES = ["posts", "comments", "albums", "photos", "todos", "users"]


@pytest.mark.parametrize("resource", RESOURCES)
def test_resource_collection_is_available(api_client: ApiClient, resource: str) -> None:
    """Goal: verify each resource collection returns a usable JSON list.

    Assertion: GET returns 200, JSON content type, and a non-empty list.
    SDET Rationale: one parametrized test maximizes route coverage with minimal duplication.
    """

    response = api_client.get(f"/{resource}")

    api_client.assert_status(response, 200)
    assert response.headers.get("Content-Type", "").startswith("application/json")
    payload = response.json()
    assert isinstance(payload, list)
    assert payload
