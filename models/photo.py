"""Pydantic contract for photo collection responses."""

from pydantic import BaseModel, ConfigDict, Field


class Photo(BaseModel):
    """Goal: validate each record returned by GET `/photos`.

    Assertion: album/id identifiers are positive and URL fields are strings.
    SDET Rationale: photo metadata is consumed by clients that depend on stable links.
    """

    model_config = ConfigDict(extra="ignore")

    albumId: int = Field(ge=1)
    id: int = Field(ge=1)
    title: str
    url: str
    thumbnailUrl: str
