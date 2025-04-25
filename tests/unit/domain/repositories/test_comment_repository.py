"""Tests for CommentRepository interface."""

import pytest
from datetime import datetime
from typing import List, Optional

from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.domain.repositories.comment_repository import CommentRepository


class TestCommentRepository:
    """Test cases for CommentRepository interface."""
    
    @pytest.mark.asyncio
    async def test_get_comments(self):
        """Test get_comments method."""
        # Create a mock repository
        class MockCommentRepository(CommentRepository):
            async def get_comments(self, subfeddit_id: int, limit: int = 10, skip: int = 0) -> List[Comment]:
                now = datetime.now()
                return [
                    Comment(
                        id=1,
                        subfeddit_id=subfeddit_id,
                        username="test_user",
                        text="Test comment",
                        created_at=now,
                        updated_at=now
                    )
                ]
            
            async def get_by_id(self, comment_id: int) -> Optional[Comment]:
                return None
            
            async def get_by_subfeddit(self, subfeddit_id: int) -> List[Comment]:
                return []
            
            async def create(self, comment: Comment) -> Comment:
                return comment
            
            async def update(self, comment: Comment) -> Comment:
                return comment
            
            async def delete(self, comment_id: int) -> bool:
                return True
        
        repo = MockCommentRepository()
        comments = await repo.get_comments(subfeddit_id=1, limit=10, skip=0)
        
        assert len(comments) == 1
        assert isinstance(comments[0], Comment)
        assert comments[0].id == 1
        assert comments[0].subfeddit_id == 1
        assert comments[0].username == "test_user"
        assert comments[0].text == "Test comment"
    
    @pytest.mark.asyncio
    async def test_get_comments_with_pagination(self):
        """Test get_comments method with pagination."""
        class MockCommentRepository(CommentRepository):
            async def get_comments(self, subfeddit_id: int, limit: int = 10, skip: int = 0) -> List[Comment]:
                now = datetime.now()
                return [
                    Comment(
                        id=i + 1,  # Ensure positive ID
                        subfeddit_id=subfeddit_id,
                        username=f"test_user_{i}",
                        text=f"Test comment {i}",
                        created_at=now,
                        updated_at=now
                    ) for i in range(skip, skip + limit)
                ]
            
            async def get_by_id(self, comment_id: int) -> Optional[Comment]:
                return None
            
            async def get_by_subfeddit(self, subfeddit_id: int) -> List[Comment]:
                return []
            
            async def create(self, comment: Comment) -> Comment:
                return comment
            
            async def update(self, comment: Comment) -> Comment:
                return comment
            
            async def delete(self, comment_id: int) -> bool:
                return True
        
        repo = MockCommentRepository()
        
        # Test first page
        comments = await repo.get_comments(subfeddit_id=1, limit=5, skip=0)
        assert len(comments) == 5
        assert comments[0].id == 1
        assert comments[-1].id == 5
        
        # Test second page
        comments = await repo.get_comments(subfeddit_id=1, limit=5, skip=5)
        assert len(comments) == 5
        assert comments[0].id == 6
        assert comments[-1].id == 10 