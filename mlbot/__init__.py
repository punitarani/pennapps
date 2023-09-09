"""
mlbot.__init__.py

mlbot package
"""

from dotenv import load_dotenv

from config import PROJECT_DIR

load_dotenv(PROJECT_DIR.joinpath(".env"))
