"""routers.upload.py"""

import io
import tempfile
from uuid import uuid4, UUID

import pandas as pd
from fastapi import FastAPI, APIRouter, Depends, HTTPException, UploadFile
from fastapi.param_functions import File

from dependencies import get_user_id
from mlbot.store import StorageBucket

app = FastAPI()

router = APIRouter(prefix="/upload", tags=["upload"])

bucket = StorageBucket("user-data")


def upload_df(df: pd.DataFrame, path_in_bucket: str) -> None:
    """Converts a DataFrame to a Parquet file and uploads it to the Supabase bucket."""
    with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as temp_file:
        try:
            df.to_parquet(temp_file.name)
            bucket.upload(source=temp_file.name, destination=path_in_bucket)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


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
    file_path_in_bucket = f"{user_id}/{fn}.parquet"

    # Upload the DataFrame as a Parquet file to the Supabase bucket
    upload_df(df, file_path_in_bucket)

    return fn
