"""mlbot.agent.py"""

from codeinterpreterapi import CodeInterpreterSession, File
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

from config import PROJECT_DIR

load_dotenv(PROJECT_DIR.joinpath(".env"))


def analyze_file(filepath: str) -> tuple[str, list[File]]:
    with CodeInterpreterSession() as session:
        # define the user request
        user_request = (
            "Explore the dataset and analyze the data. Concisely summarize the data and their features. "
            "Approach the dataset from different angles to gain some preliminary understanding of the data. "
            "The analysis must be thorough, diverse, and insightful enough to be useful for the data science team. "
            "Generate at least a few insightful visualizations with a brief explanation of what they show. "
        )
        files = [
            File.from_path(filepath),
        ]

        # generate the response
        response = session.generate_response_sync(user_request, files=files)

        # Output to the user
        # print("AI: ", response.content)
        # for file in response.files:
        #     file.show_image()

        return response.content, response.files
