"""mlbot.errors.py"""

from uuid import UUID

from mlbot.models import FileType


class DataNotAvailable(Exception):
    """Data not available error"""

    def __init__(self, user_id: str, file_id: str, file_type: FileType) -> None:
        """
        Initialize DataNotAvailable exception.

        Args:
            user_id (UUID): User ID
            file_id (UUID): File ID
        """

        super().__init__(
            f"Data not available for user_id={user_id}, file_id={file_id}, file_type={file_type.value}"
        )
