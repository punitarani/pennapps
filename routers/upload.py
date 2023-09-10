"""routers.upload.py"""

import io
from pathlib import Path
from uuid import uuid4, UUID

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.param_functions import File

from config import DATA_DIR
from dependencies import get_user_id

router = APIRouter(prefix="/upload", tags=["upload"])


def upload_df(df: pd.DataFrame, filepath: str) -> None:
    """Converts a DataFrame to a Parquet file and uploads it to the Supabase bucket."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(filepath)


@router.post("/csv/")
async def upload_csv(
    file: UploadFile = File(...), user_id: UUID = Depends(get_user_id)
) -> UUID:
    # Check if the uploaded file is a CSV
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only .csv files are allowed."
        )

    # Read the uploaded file into a DataFrame
    file_contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(file_contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error reading CSV: " + str(e))

    # Create a unique filename
    fn = uuid4()

    # Define the file path in the bucket
    filepath = DATA_DIR.joinpath("users", str(user_id), f"{fn}.parquet")

    # Upload the DataFrame as a Parquet file to the Supabase bucket
    upload_df(df, filepath)

    return fn
