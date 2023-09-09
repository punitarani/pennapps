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
        if self.file_type in [FileType.CSV]:
            self.data = self.load_file()

    @property
    def filepath(self) -> Path:
        """
        Return the CSV file path.

        Returns:
            str: CSV file path
        """

        return DATA_DIR.joinpath(self.user_id, f"{self.file_id}.parquet")

    def load_file(self) -> pd.DataFrame:
        """
        Load file.

        Returns:
            pd.DataFrame: File data
        """

        if self.file_type == FileType.CSV:
            return pd.read_parquet(self.filepath)
        else:
            raise DataNotAvailable(
                user_id=self.user_id, file_id=self.file_id, file_type=self.file_type
            )
