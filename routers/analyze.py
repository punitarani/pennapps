"""routers.analyze.py"""

from uuid import UUID

from fastapi import FastAPI, APIRouter, Depends

from config import DATA_DIR
from dependencies import get_user_id
from mlbot.agent import analyze_file

app = FastAPI()

router = APIRouter(prefix="/analyze", tags=["analyze"])


@router.get("/{file_id}")
async def _analyze_file(
    file_id: UUID,
    user_id: UUID = Depends(get_user_id),
):
    response = analyze_file(f"data/users/{user_id}/{file_id}.parquet")
    return {
        "answer": response[0],
        "files": response[1],
    }
