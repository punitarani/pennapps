"""mlbot.mlbot.py"""

import json
from copy import deepcopy
from pathlib import Path
from uuid import UUID

import openai
import pandas as pd

from config import DATA_DIR
from mlbot.errors import DataNotAvailable
from mlbot.models import FileType
from mlbot.utils import load_prompts, load_prompt_messages, load_prompt_functions

PROMPTS = load_prompts()
PROMPT_MESSAGES = load_prompt_messages()
PROMPT_FUNCTIONS = load_prompt_functions()


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

        return DATA_DIR.joinpath("users", self.user_id, f"{self.file_id}.parquet")

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

    async def query_file(self, query: str) -> str:
        df = deepcopy(self.data)

        base_prompt = PROMPTS["MLBot.query_file"]
        messages = [{"role": "user", "content": df.describe().to_string()}]
        functions = PROMPT_FUNCTIONS["MLBot.task_to_python"]

        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a smart Data Scientist tasked with writing efficient"
                    " and accurate python and pandas queries to solve the following task.",
                },
                {
                    "role": "user",
                    "content": base_prompt.format(task=query),
                },
                *messages,
            ],
            temperature=0.4,
            max_tokens=256,
            functions=functions,
            function_call={"name": "task_to_python"},
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        python_code = json.loads(
            response["choices"][0]["message"]["function_call"]["arguments"]
        )["python"]
        kwargs = {"df": df}

        result = await self.execute_py(code=python_code, **kwargs)

        return result

    @staticmethod
    async def execute_py(code, **kwargs) -> str:
        """
        Execute Python code.

        Args:
            code (str): Python code to be executed
            **kwargs: Arbitrary keyword arguments

        Returns:
            str: Execution result
        """

        local_vars = {**kwargs}
        try:
            # If there are other IO-bound operations here, use appropriate async methods
            result = eval(code, {}, local_vars)
        except SyntaxError:
            exec(code, {}, local_vars)
            result = local_vars.get("result", "Execution completed successfully")
        except Exception as e:
            result = str(e)

        return result
