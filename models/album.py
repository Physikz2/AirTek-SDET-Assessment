"""Pydantic contract for album collection responses."""

from pydantic import BaseModel, ConfigDict, Field


class Album(BaseModel):
    """Goal: validate each record returned by GET `/albums`.

    Assertion: userId and id are positive integers and title is text.
    SDET Rationale: resource-level contracts detect field type drift early.
    """

    model_config = ConfigDict(extra="ignore")

    userId: int = Field(ge=1)
    id: int = Field(ge=1)
    title: str
