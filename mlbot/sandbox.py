"""mlbot.sandbox.py"""

import docker
import pandas as pd
import os


class Sandbox:
    def __init__(self, session_id: str, dataframe: pd.DataFrame):
        self.session_id = session_id
        self.dataframe = dataframe
        self.container = None
        self.client = docker.from_env()

        # Check if a container with this session_id already exists
        for cont in self.client.containers.list(all=True):
            if cont.name == self.session_id:
                self.container = cont
                break

    def start(self):
        if not self.container:
            # Start a new container
            self.container = self.client.containers.run(
                "mlbot-sandbox", name=self.session_id, detach=True, remove=True
            )
            # Initialize the dataframe inside the container
            self.init_df()

        elif self.container.status != "running":
            # If the container exists but is not running, start it
            self.container.start()

    def stop(self):
        if self.container and self.container.status == "running":
            self.container.stop()

    def init_df(self):
        parquet_fp = f"{self.session_id}.parquet"
        self.dataframe.to_parquet(parquet_fp, index=False)

        # Now, we can copy this Parquet file into the Docker container
        with open(parquet_fp, "rb") as f:
            self.container.put_archive("/app/", f.read())

        os.remove(parquet_fp)

    def execute(self, code: str):
        self.start()

        # Prepend code to import pandas and read the Parquet file into a dataframe named df
        prepended_code = (
            "import pandas as pd\n"
            f"df = pd.read_parquet('/app/{self.session_id}.parquet')\n"
            f"{code}"
        )

        # Escape the single quotes in the code to be executed
        escaped_code = prepended_code.replace("'", r"\'")

        # Execute the prepended code inside the container
        exit_code, output = self.container.exec_run(f"python -c '{escaped_code}'")

        # Optionally, stop the container after executing the code
        self.stop()

        # Handle the exit code and output appropriately
        if exit_code == 0:
            return output.decode("utf-8")
        else:
            raise Exception(
                f"Error in execution. Code: {exit_code}, Output: {output.decode('utf-8')}"
            )
