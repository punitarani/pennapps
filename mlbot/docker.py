"""mlbot.docker.py"""


import json
import os
import tempfile
from uuid import uuid4

import docker

from mlbot.utils import load_exec_code


class DockerExecutor:
    """Handles Docker operations for executing Python code."""

    def __init__(self, image_name="mlbot-sandbox", container_name=None):
        self.client = docker.from_env()
        self.image_name = image_name
        self.container_name = container_name or f"PennApps_{uuid4()}"

    def run(self, code, df):
        # Serialize the DataFrame to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as temp:
            df.to_parquet(temp.name)
            temp_file_path = temp.name

        # Convert the code and DataFrame path to JSON
        data = json.dumps({"code": code, "kwargs": {"df": "/tmp/data.parquet"}})

        # Prepare the Python code to read the DataFrame and execute the given code
        python_execution_code = load_exec_code("DockerExecutor.run").replace(
            "{data}", data
        )

        # Use docker-py to run the Docker container
        logs = self.client.containers.run(
            image=self.image_name,
            command=["python", "-c", python_execution_code],
            volumes={temp_file_path: {"bind": "/tmp/data.parquet", "mode": "ro"}},
            remove=True,
            mem_limit="512m",
            network_mode="none",
            name=self.container_name,
            stdout=True,
            stderr=True,
        ).decode("utf-8")

        # Cleanup: Remove the temporary file
        os.remove(temp_file_path)

        return logs
