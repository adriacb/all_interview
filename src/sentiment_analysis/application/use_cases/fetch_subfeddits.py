"""Use case for fetching subfeddits."""
from typing import List

from sentiment_analysis.domain.entities.subfeddit import Subfeddit
from sentiment_analysis.domain.repositories.subfeddit_repository import SubfedditRepository
from sentiment_analysis.logger import configure_logger


class FetchSubfedditsUseCase:
    """Use case for fetching subfeddits.

    This use case handles the business logic for fetching subfeddits from the repository.
    """

    def __init__(self, subfeddit_repository: SubfedditRepository):
        """Initialize the use case.

        Args:
            subfeddit_repository: Repository for fetching subfeddits.
        """
        self.subfeddit_repository = subfeddit_repository
        self.logger = configure_logger().bind(use_case="fetch_subfeddits")

    async def execute(self, limit: int = 10, skip: int = 0) -> List[Subfeddit]:
        """Execute the use case.

        Args:
            limit: Maximum number of subfeddits to return. Defaults to 10.
            skip: Number of subfeddits to skip. Defaults to 0.

        Returns:
            List of Subfeddit objects.

        Raises:
            Exception: If an error occurs while fetching subfeddits.
        """
        self.logger.info(
            "Fetching subfeddits",
            limit=limit,
            skip=skip
        )
        try:
            subfeddits = await self.subfeddit_repository.get_subfeddits(
                limit=limit,
                skip=skip
            )
            self.logger.info(
                "Successfully fetched subfeddits",
                count=len(subfeddits)
            )
            return subfeddits
        except Exception as e:
            self.logger.error(
                "Failed to fetch subfeddits",
                error=str(e)
            )
            raise
