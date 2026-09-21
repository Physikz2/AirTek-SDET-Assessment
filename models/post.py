"""Pydantic contracts for post collection responses and create payloads."""

from pydantic import BaseModel, ConfigDict, Field


class Post(BaseModel):
    """Goal: validate the required shape of a GET `/posts` record.

    Assertion: IDs are positive integers and title/body are strings.
    SDET Rationale: contract validation catches breaking API changes before consumers fail.
    """

    # Ignore additive fields so harmless server extensions do not break clients.
    model_config = ConfigDict(extra="ignore")

    userId: int = Field(ge=1)
    id: int = Field(ge=1)
    title: str
    body: str


class PostCreate(BaseModel):
    """Goal: validate the payload sent to POST `/posts`.

    Assertion: userId, title, and body are present with their expected types.
    SDET Rationale: request contracts prevent malformed test data from masking API defects.
    """

    model_config = ConfigDict(extra="ignore")

    userId: int = Field(ge=1)
    title: str
    body: str
