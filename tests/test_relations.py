"""Relationship and query-parameter integrity tests for JSONPlaceholder resources."""

import pytest
from client.api_client import ApiClient


def test_comments_can_be_filtered_by_post_id(api_client: ApiClient) -> None:
    """Goal: validate GET `/comments?postId=1` filtering.

    Assertion: response is 200, non-empty, and every comment has postId 1.
    SDET Rationale: query filtering must not leak records from unrelated parent resources.
    """
    response = api_client.get("/comments", params={"postId": 1})
    api_client.assert_status(response, 200)

    comments = response.json()
    assert len(comments) > 0
    assert all(comment["postId"] == 1 for comment in comments)


@pytest.mark.parametrize(
    "endpoint, parent_key, expected_parent_id",
    [
        ("/posts/1/comments", "postId", 1),
        ("/albums/1/photos", "albumId", 1),
        ("/users/1/albums", "userId", 1),
        ("/users/1/todos", "userId", 1),
        ("/users/1/posts", "userId", 1),
    ],
)
def test_nested_resource_routes(
    api_client: ApiClient,
    endpoint: str,
    parent_key: str,
    expected_parent_id: int,
) -> None:
    """Goal: validate nested resource sub-routes across all available relations.

    Assertion: response status is 200, payload is non-empty, and every child item
               contains a matching parent foreign key.
    SDET Rationale: validates parent-child resource hierarchy and routing integrity.
    """
    response = api_client.get(endpoint)
    api_client.assert_status(response, 200)

    records = response.json()
    assert len(records) > 0
    assert all(item[parent_key] == expected_parent_id for item in records)