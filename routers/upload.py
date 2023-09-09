"""routers.upload.py"""

from uuid import uuid4, UUID

from fastapi import FastAPI, APIRouter, HTTPException, UploadFile
from fastapi.param_functions import File

from config import DATA_DIR

app = FastAPI()

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/csv/")
async def upload_csv(user_id: UUID, file: UploadFile = File(...)) -> UUID:
    # Check if the uploaded file is a CSV
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only .csv files are allowed."
        )

    # Create a unique filename
    fn = uuid4()

    # Define the file path
    user_dir = DATA_DIR.joinpath(str(user_id))
    user_dir.mkdir(parents=False, exist_ok=True)
    fp = user_dir.joinpath(f"{fn}.csv")

    # Save the file to disk
    try:
        file_contents = await file.read()
        with fp.open("wb") as f:
            f.write(file_contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return fn
