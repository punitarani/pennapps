"""mlbot.agent.py"""

from codeinterpreterapi import CodeInterpreterSession, File
from codeinterpreterapi.schema import CodeInterpreterResponse
from dotenv import load_dotenv

from config import PROJECT_DIR

load_dotenv(PROJECT_DIR.joinpath(".env"))


async def analyze_file(filepath: str) -> CodeInterpreterResponse:
    async with CodeInterpreterSession() as session:
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
        response = await session.agenerate_response(user_request, files=files)

        # Output to the user
        # print("AI: ", response.content)
        # for file in response.files:
        #     file.show_image()

        return response


async def analyze_ml_models(filepath: str) -> list[CodeInterpreterResponse]:
    async with CodeInterpreterSession() as session:
        # define the user request
        user_request = (
            "Help me build, train, and evaluate machine learning models for this dataset. "
            "The models must be able to predict the target variable with high accuracy. "
            "You are a great data scientist, so you can use any model you want. "
            "You can use any machine learning algorithm and library you want. "
            "Continue to improve the models until you are satisfied with the results. "
            "Feel free to iterate through different models and hyperparameters. "
            "You need to answer step-by-step how you built the models and why you chose them. "
            "You are given memory and you therefore do not need to worry about solving the problem in one go. "
            "Only once you are satisfied with the results, return only '<DONE>' as the answer."
            "However, you are only given {STEPS} steps to solve this problem. This is step {STEP}."
        )

        files = [
            File.from_path(filepath),
        ]

        responses = []
        response = ""
        max_steps = 12
        step = 0
        while "<DONE>" not in response and step < max_steps:
            step += 1
            # generate the response
            response = await session.agenerate_response(
                user_request.format(STEPS=max_steps, STEP=step), files=files
            )
            responses.append(response)

            # Output to the user
            # print("AI: ", response.content)
            # for file in response.files:
            #     file.show_image()

        return responses
