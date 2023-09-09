"""
mlbot.__init__.py

mlbot package
"""

import os

import openai
from dotenv import load_dotenv
from supabase import create_client, Client

from config import PROJECT_DIR

load_dotenv(PROJECT_DIR.joinpath(".env"))

# Configure OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_API_KEY, "OPENAI_API_KEY environment variable not set"
openai.api_key = OPENAI_API_KEY

# Configure Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_DB_HOST = os.getenv("SUPABASE_DB_HOST")
SUPABASE_DB_PORT = os.getenv("SUPABASE_DB_PORT")
SUPABASE_DB_NAME = os.getenv("SUPABASE_DB_NAME")
SUPABASE_DB_USER = os.getenv("SUPABASE_DB_USER")
SUPABASE_DB_PASS = os.getenv("SUPABASE_DB_PASS")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

for var in [
    SUPABASE_URL,
    SUPABASE_ANON_KEY,
    SUPABASE_SERVICE_ROLE_KEY,
    SUPABASE_DB_HOST,
    SUPABASE_DB_PORT,
    SUPABASE_DB_NAME,
    SUPABASE_DB_USER,
    SUPABASE_DB_PASS,
    SUPABASE_JWT_SECRET,
]:
    assert var, f"{var} environment variable not set"

supabase: Client = create_client(
    supabase_url=SUPABASE_URL, supabase_key=SUPABASE_SERVICE_ROLE_KEY
)
