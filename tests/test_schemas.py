"""Contract validation tests for every record in all six API collections."""

import pytest
from pydantic import BaseModel

from client.api_client import ApiClient
from models.album import Album
from models.comment import Comment
from models.photo import Photo
from models.post import Post
from models.todo import Todo
from models.user import User


SCHEMA_CASES = [
    ("posts", Post),
    ("comments", Comment),
    ("albums", Album),
    ("photos", Photo),
    ("todos", Todo),
    ("users", User),
]


@pytest.mark.parametrize("resource, model", SCHEMA_CASES)
def test_collection_records_match_contract(
    api_client: ApiClient, resource: str, model: type[BaseModel]
) -> None:
    """Goal: validate every record from one resource against its Pydantic model.

    Assertion: the collection is successful, non-empty, and every record instantiates.
    SDET Rationale: exhaustive response validation detects schema drift across full data sets.
    """

    response = api_client.get(f"/{resource}")
    api_client.assert_status(response, 200)

    records = response.json()
    assert records
    for record in records:
        validated = model.model_validate(record)
        assert isinstance(validated, model)
