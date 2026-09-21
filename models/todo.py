"""Pydantic contract for todo collection responses."""

from pydantic import BaseModel, ConfigDict, Field


class Todo(BaseModel):
    """Goal: validate each record returned by GET `/todos`.

    Assertion: identifiers are positive, title is text, and completed is boolean.
    SDET Rationale: strict primitive types prevent UI and workflow state corruption.
    """

    model_config = ConfigDict(extra="ignore")

    userId: int = Field(ge=1)
    id: int = Field(ge=1)
    title: str
    completed: bool
