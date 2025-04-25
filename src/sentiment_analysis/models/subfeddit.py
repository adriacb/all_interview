"""Subfeddit model for Feddit API."""

from pydantic import BaseModel, Field


class Subfeddit(BaseModel):
    """Model representing a subfeddit from Feddit.

    Attributes:
        id: Unique identifier of the subfeddit.
        username: User who created the subfeddit.
        title: Title of the subfeddit.
        description: Description of the subfeddit.
    """

    id: int = Field(..., description="Unique identifier of the subfeddit")
    username: str = Field(..., description="User who created the subfeddit")
    title: str = Field(..., description="Title of the subfeddit")
    description: str = Field(..., description="Description of the subfeddit") 