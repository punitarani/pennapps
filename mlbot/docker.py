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
        self.container = None

        self.temp_file_path = None

    def create(self, df):
        # Serialize the DataFrame to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as temp:
            df.to_parquet(temp.name)
            self.temp_file_path = temp.name

        # Setup the container with necessary configuration
        self.container = self.client.containers.create(
            image=self.image_name,
            command=[
                "python",
                "-c",
                "while True: pass",
            ],  # Infinite loop to keep the container running
            volumes={self.temp_file_path: {"bind": "/tmp/data.parquet", "mode": "ro"}},
            mem_limit="512m",
            network_mode="none",
            name=self.container_name,
        )

    def start(self):
        # Start the container
        self.container.start()

    def stop(self):
        # Stop the container
        self.container.stop()

        # Cleanup: Remove the temporary file
        os.remove(self.temp_file_path)

        # Remove the container
        self.container.remove()

    def execute(self, code):
        # Convert the code and DataFrame path to JSON
        data = json.dumps({"code": code, "kwargs": {"df": "/tmp/data.parquet"}})

        # Prepare the Python code to read the DataFrame and execute the given code
        python_execution_code = load_exec_code("DockerExecutor.run").replace(
            "{data}", data
        )

        # Execute the command in the running container
        _, logs = self.container.exec_run(["python", "-c", python_execution_code])

        return logs.decode("utf-8")
