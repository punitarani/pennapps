"""
mlbot.__init__.py

mlbot package
"""

import os

import openai
from dotenv import load_dotenv

from config import PROJECT_DIR

load_dotenv(PROJECT_DIR.joinpath(".env"))

# Configure OpenAI API key
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY environment variable not set"
openai.api_key = os.getenv("OPENAI_API_KEY")
