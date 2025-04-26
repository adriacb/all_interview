"""Subfeddit domain entity."""

from pydantic import BaseModel, Field, field_validator
from pydantic_core._pydantic_core import ValidationError


class Subfeddit(BaseModel):
    """Subfeddit domain entity."""
    
    id: int = Field(gt=0)
    username: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str
    
    @field_validator('id')
    @classmethod
    def validate_id(cls, v):
        """Validate that id is a positive integer."""
        if not isinstance(v, int) or v <= 0:
            raise ValueError('id must be a positive integer')
        return v
    
    @field_validator('username', 'title')
    @classmethod
    def validate_string_fields(cls, v):
        """Validate that string fields are non-empty."""
        if not v.strip():
            raise ValidationError("Field must not be empty")
        return v.strip()
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        """Validate that description is a string."""
        if not isinstance(v, str):
            raise ValidationError("Description must be a string")
        return v
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "test_user",
                "title": "Test Subfeddit",
                "description": "A test subfeddit"
            }
        }
