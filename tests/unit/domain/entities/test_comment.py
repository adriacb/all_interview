"""Tests for Comment domain entity."""

import pytest
from datetime import datetime
from pydantic_core._pydantic_core import ValidationError

from sentiment_analysis.domain.entities.comment import Comment


def test_create_valid_comment():
    """Test creating a valid Comment."""
    now = datetime.now()
    comment = Comment(
        id=1,
        subfeddit_id=2,
        username="test_user",
        text="Test comment",
        created_at=now,
        updated_at=now
    )
    
    assert comment.id == 1
    assert comment.subfeddit_id == 2
    assert comment.username == "test_user"
    assert comment.text == "Test comment"
    assert comment.created_at == now
    assert comment.updated_at == now


def test_create_invalid_comment():
    """Test creating an invalid Comment."""
    now = datetime.now()
    
    # Test invalid id
    with pytest.raises(ValidationError):
        Comment(
            id=0,  # Invalid: must be positive
            subfeddit_id=2,
            username="test_user",
            text="Test comment",
            created_at=now,
            updated_at=now
        )
    
    # Test invalid subfeddit_id
    with pytest.raises(ValidationError):
        Comment(
            id=1,
            subfeddit_id=0,  # Invalid: must be positive
            username="test_user",
            text="Test comment",
            created_at=now,
            updated_at=now
        )
    
    # Test invalid username
    with pytest.raises(ValidationError):
        Comment(
            id=1,
            subfeddit_id=2,
            username="",  # Invalid: empty string
            text="Test comment",
            created_at=now,
            updated_at=now
        )
    
    # Test invalid text
    with pytest.raises(ValidationError):
        Comment(
            id=1,
            subfeddit_id=2,
            username="test_user",
            text="",  # Invalid: empty string
            created_at=now,
            updated_at=now
        )
    
    # Test invalid datetime
    with pytest.raises(ValidationError):
        Comment(
            id=1,
            subfeddit_id=2,
            username="test_user",
            text="Test comment",
            created_at="invalid_datetime",  # Invalid: not a datetime
            updated_at=now
        )
