"""mlbot.utils.py"""

import json
from pathlib import Path
from types import MappingProxyType


def load_prompts() -> MappingProxyType[str, str]:
    """
    Load the prompts from the prompts.json file.

    Returns:
        A dictionary of prompts.
        It is a mapping proxy type, so it is immutable.
    """

    prompts_dir = Path(__file__).parent.joinpath("prompts")

    prompt_files = ["MLBot.query_file"]

    # Load the prompts from each file
    prompts = {}
    for prompt_file in prompt_files:
        with open(prompts_dir.joinpath(prompt_file), "r") as f:
            prompts[prompt_file] = f.read()

    return MappingProxyType(prompts)


def load_prompt_functions() -> MappingProxyType[str, str]:
    """
    Load the prompt functions from the functions.json file.

    Returns:
        A dictionary of prompt functions.
        It is a mapping proxy type, so it is immutable.
    """

    prompts_dir = Path(__file__).parent.joinpath("prompts")
    prompt_functions_fp = prompts_dir.joinpath("functions.json")

    functions = ["MLBot.task_to_python"]

    with open(prompt_functions_fp, "r") as f:
        prompt_functions = f.read()

    # Ensure all functions are in the functions.json file
    for function in functions:
        assert (
            function in prompt_functions
        ), f"Function {function} not in functions.json"

    return MappingProxyType(json.loads(prompt_functions))


def load_prompt_messages() -> MappingProxyType[str, str]:
    """
    Load the prompt messages from the messages.json file.

    Returns:
        A dictionary of prompt messages.
        It is a mapping proxy type, so it is immutable.
    """

    prompts_dir = Path(__file__).parent.joinpath("prompts")
    prompt_messages_fp = prompts_dir.joinpath("messages.json")

    messages = []

    with open(prompt_messages_fp, "r") as f:
        prompt_messages = f.read()

    # Ensure all messages are in the messages.json file
    for message in messages:
        assert message in prompt_messages, f"Message {message} not in messages.json"

    return MappingProxyType(json.loads(prompt_messages))


def load_exec_code(filename: str) -> str:
    """
    Load the Python execution code from the given filename.

    Args:
        filename (str): Name of the file to load the code from.

    Returns:
        str: Python execution code as a string.
    """

    code_dir = Path(__file__).parent.joinpath("exec_codes")
    with open(code_dir.joinpath(filename), "r") as f:
        code = f.read()

    return code
