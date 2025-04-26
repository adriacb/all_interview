"""Tests for Subfeddit domain entity."""

import pytest
from pydantic_core._pydantic_core import ValidationError

from sentiment_analysis.domain.entities.subfeddit import Subfeddit


def test_create_valid_subfeddit():
    """Test creating a valid Subfeddit."""
    subfeddit = Subfeddit(
        id=1,
        username="test_user",
        title="Test Title",
        description="Test Description"
    )
    
    assert subfeddit.id == 1
    assert subfeddit.username == "test_user"
    assert subfeddit.title == "Test Title"
    assert subfeddit.description == "Test Description"


def test_create_invalid_subfeddit():
    """Test creating an invalid Subfeddit."""
    # Test invalid id
    with pytest.raises(ValidationError):
        Subfeddit(
            id=0,  # Invalid: must be positive
            username="test_user",
            title="Test Title",
            description="Test Description"
        )
    
    # Test invalid username
    with pytest.raises(ValidationError):
        Subfeddit(
            id=1,
            username="",  # Invalid: empty string
            title="Test Title",
            description="Test Description"
        )
    
    # Test invalid title
    with pytest.raises(ValidationError):
        Subfeddit(
            id=1,
            username="test_user",
            title="",  # Invalid: empty string
            description="Test Description"
        )
    
    # Test invalid description
    with pytest.raises(ValidationError):
        Subfeddit(
            id=1,
            username="test_user",
            title="Test Title",
            description=123  # Invalid: not a string
        )
