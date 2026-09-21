"""Pydantic contract for comment collection and relationship responses."""

from pydantic import BaseModel, ConfigDict, Field


class Comment(BaseModel):
    """Goal: validate records returned by GET `/comments` and related routes.

    Assertion: post and comment IDs are positive and content fields are strings.
    SDET Rationale: stable comment contracts protect relational and consumer workflows.
    """

    model_config = ConfigDict(extra="ignore")

    postId: int = Field(ge=1)
    id: int = Field(ge=1)
    name: str
    email: str
    body: str
