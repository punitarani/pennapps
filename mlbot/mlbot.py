"""mlbot.mlbot.py"""

import json
import os
import subprocess
import tempfile
from copy import deepcopy
from pathlib import Path

from uuid import UUID, uuid4

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
        Execute Python code inside a Docker container.

        Args:
            code (str): Python code to be executed
            **kwargs: Arbitrary keyword arguments

        Returns:
            str: Execution result
        """

        # Serialize the DataFrame to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as temp:
            kwargs["df"].to_parquet(temp.name)
            temp_file_path = temp.name

        # Convert the code and kwargs to JSON
        data = json.dumps({"code": code, "kwargs": {"df": "/tmp/data.parquet"}})

        # Prepare the Python code to read the DataFrame and execute the given code
        python_execution_code = f"""
import pandas as pd
import json
df = pd.read_parquet("/tmp/data.parquet")
data = json.loads('{data}')
if "\\n" in data["code"] or "=" in data["code"]:
    exec(data["code"])
else:
    result = eval(data["code"])
    print(result)
"""

        # Execute the Docker command
        docker_command = [
            "docker",
            "run",
            "--rm",
            "--name",
            f"PennApps_{uuid4()}",
            "--network",
            "none",
            "--memory",
            "512m",
            "--cpus",
            "1",
            "-v",
            f"{temp_file_path}:/tmp/data.parquet",
            "mlbot-sandbox",
            "python",
            "-c",
            python_execution_code,
        ]

        result = subprocess.run(docker_command, capture_output=True, text=True)

        # Cleanup: Remove the temporary file
        os.remove(temp_file_path)

        # If there's an error in the Docker command or the Python code, it'll be in stderr
        if result.stderr:
            return result.stderr

        return result.stdout
