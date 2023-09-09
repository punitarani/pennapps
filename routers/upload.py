"""routers.upload.py"""

import io
from uuid import uuid4, UUID

import pandas as pd
from fastapi import FastAPI, APIRouter, Depends, HTTPException, UploadFile
from fastapi.param_functions import File

from config import DATA_DIR
from dependencies import get_user_id

app = FastAPI()

router = APIRouter(prefix="/upload", tags=["upload"])


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

    # Define the file path
    user_dir = DATA_DIR.joinpath("users", str(user_id))
    user_dir.mkdir(parents=False, exist_ok=True)
    fp = user_dir.joinpath(f"{fn}.parquet")

    # Save the DataFrame as a Parquet file
    try:
        df.to_parquet(fp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return fn
