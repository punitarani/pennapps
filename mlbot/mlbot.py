"""mlbot.mlbot.py"""

from pathlib import Path
from uuid import UUID

import pandas as pd

from config import DATA_DIR
from mlbot.errors import DataNotAvailable
from mlbot.models import FileType


class MLBot:
    """ML Bot"""

    def __init__(
        self, user_id: UUID, file_id: UUID, file_type: FileType = FileType.CSV
    ) -> None:
        """
        Initialize ML Bot.

        Args:
            user_id (UUID): User ID
            file_id (UUID): File ID
        """

        self.user_id = str(user_id)
        self.file_id = str(file_id)
        self.file_type = file_type
