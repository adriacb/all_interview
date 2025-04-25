"""Comment model for Feddit API."""

from pydantic import BaseModel, Field


class Comment(BaseModel):
    """Model representing a comment from Feddit.

    Attributes:
        id: Unique identifier of the comment.
        username: User who made the comment.
        text: Content of the comment.
        created_at: Unix epoch timestamp of when the comment was created.
    """

    id: int = Field(..., description="Unique identifier of the comment")
    username: str = Field(..., description="User who made the comment")
    text: str = Field(..., description="Content of the comment")
    created_at: int = Field(
        ...,
        description="Unix epoch timestamp of when the comment was created"
    ) 