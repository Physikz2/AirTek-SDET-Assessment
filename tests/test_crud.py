"""Write-operation tests for the simulated `/posts` CRUD surface."""

from client.api_client import ApiClient


POST_PATH = "/posts"
POST_ID_PATH = "/posts/1"


def assert_json_response(api_client: ApiClient, response, expected_status: int) -> dict:
    """Goal: apply common status, header, and object assertions to write responses.

    Assertion: status and JSON content type match expectations and the body is an object.
    SDET Rationale: shared checks keep CRUD tests focused on operation-specific payloads.
    """

    api_client.assert_status(response, expected_status)
    assert response.headers.get("Content-Type", "").startswith("application/json")
    payload = response.json()
    assert isinstance(payload, dict)
    return payload


def test_create_post(api_client: ApiClient, post_payload: dict[str, object]) -> None:
    """Goal: validate POST `/posts` creation response and echoed fields.

    Assertion: response is 201, contains JSON, echoes the payload, and has an integer ID.
    SDET Rationale: verifies creation semantics without assuming mock persistence.
    """

    payload = assert_json_response(api_client, api_client.post(POST_PATH, json=post_payload), 201)

    assert payload["userId"] == post_payload["userId"]
    assert payload["title"] == post_payload["title"]
    assert payload["body"] == post_payload["body"]
    assert isinstance(payload["id"], int)


def test_replace_post(api_client: ApiClient, post_payload: dict[str, object]) -> None:
    """Goal: validate PUT `/posts/1` replacement semantics.

    Assertion: response is 200 and preserves ID plus replacement title/body values.
    SDET Rationale: confirms the full-update contract at the API boundary.
    """

    payload = assert_json_response(api_client, api_client.put(POST_ID_PATH, json={"id": 1, **post_payload}), 200)

    assert payload["id"] == 1
    assert payload["title"] == post_payload["title"]
    assert payload["body"] == post_payload["body"]


def test_update_post(api_client: ApiClient) -> None:
    """Goal: validate PATCH `/posts/1` partial-update semantics.

    Assertion: response is 200, identifies post 1, and contains the updated title.
    SDET Rationale: partial updates must preserve resource identity while changing one field.
    """

    payload = assert_json_response(api_client, api_client.patch(POST_ID_PATH, json={"title": "Updated title"}), 200)

    assert payload["id"] == 1
    assert payload["title"] == "Updated title"


def test_delete_post(api_client: ApiClient) -> None:
    """Goal: validate DELETE `/posts/1` completion semantics.

    Assertion: the API returns HTTP 200 for the simulated deletion.
    SDET Rationale: verifies the documented mock API write contract without persistence checks.
    """

    response = api_client.delete(POST_ID_PATH)

    api_client.assert_status(response, 200)
