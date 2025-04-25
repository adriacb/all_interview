"""Tests for Subfeddit domain entity."""

import pytest
from datetime import datetime
from pydantic_core._pydantic_core import ValidationError

from sentiment_analysis.domain.entities.subfeddit import Subfeddit


def test_create_valid_subfeddit():
    """Test creating a valid Subfeddit."""
    now = datetime.now()
    subfeddit = Subfeddit(
        id=1,
        username="test_user",
        title="Test Title",
        description="Test Description",
        created_at=now,
        updated_at=now
    )
    
    assert subfeddit.id == 1
    assert subfeddit.username == "test_user"
    assert subfeddit.title == "Test Title"
    assert subfeddit.description == "Test Description"
    assert subfeddit.created_at == now
    assert subfeddit.updated_at == now


def test_create_invalid_subfeddit():
    """Test creating an invalid Subfeddit."""
    now = datetime.now()
    
    # Test invalid id
    with pytest.raises(ValidationError):
        Subfeddit(
            id=0,  # Invalid: must be positive
            username="test_user",
            title="Test Title",
            description="Test Description",
            created_at=now,
            updated_at=now
        )
    
    # Test invalid username
    with pytest.raises(ValidationError):
        Subfeddit(
            id=1,
            username="",  # Invalid: empty string
            title="Test Title",
            description="Test Description",
            created_at=now,
            updated_at=now
        )
    
    # Test invalid title
    with pytest.raises(ValidationError):
        Subfeddit(
            id=1,
            username="test_user",
            title="",  # Invalid: empty string
            description="Test Description",
            created_at=now,
            updated_at=now
        )
    
    # Test invalid description
    with pytest.raises(ValidationError):
        Subfeddit(
            id=1,
            username="test_user",
            title="Test Title",
            description=123,  # Invalid: not a string
            created_at=now,
            updated_at=now
        )
    
    # Test invalid datetime
    with pytest.raises(ValidationError):
        Subfeddit(
            id=1,
            username="test_user",
            title="Test Title",
            description="Test Description",
            created_at="invalid_datetime",  # Invalid: not a datetime
            updated_at=now
        ) 