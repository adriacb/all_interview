"""Comment domain entity."""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from pydantic_core._pydantic_core import ValidationError


class Comment(BaseModel):
    """Comment domain entity."""
    
    id: int = Field(gt=0, description="Unique identifier for the comment")
    subfeddit_id: int = Field(gt=0, description="ID of the subfeddit this comment belongs to")
    username: str = Field(min_length=1, description="Username of the comment author")
    text: str = Field(min_length=1, description="Content of the comment")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime | None = Field(default=None, description="Last update timestamp")
    
    @field_validator('id')
    @classmethod
    def validate_id(cls, v):
        """Validate that id is a positive integer."""
        if not isinstance(v, int) or v <= 0:
            raise ValueError('id must be a positive integer')
        return v
    
    @field_validator('subfeddit_id')
    @classmethod
    def validate_subfeddit_id(cls, v):
        """Validate that subfeddit_id is a positive integer."""
        if not isinstance(v, int) or v <= 0:
            raise ValueError('subfeddit_id must be a positive integer')
        return v
    
    @field_validator('username', 'text')
    @classmethod
    def validate_string_fields(cls, v):
        """Validate that string fields are non-empty."""
        if not v.strip():
            raise ValidationError("Field must not be empty")
        return v.strip()
    
    @field_validator('created_at', 'updated_at')
    @classmethod
    def validate_datetime(cls, v):
        """Validate that the value is a datetime."""
        if v is None:
            return None
        if not isinstance(v, datetime):
            raise ValidationError("must be a datetime")
        return v
    
    def model_post_init(self, *args, **kwargs):
        """Set updated_at to created_at if not provided."""
        if self.updated_at is None:
            self.updated_at = self.created_at
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "subfeddit_id": 1,
                "username": "test_user",
                "text": "This is a test comment",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        } 