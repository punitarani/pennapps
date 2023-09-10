"""routers.analyze.py"""

import base64
import io
from uuid import UUID

import matplotlib.pyplot as plt
from fastapi import FastAPI, APIRouter, Depends

from dependencies import get_user_id
from mlbot.agent import analyze_file

app = FastAPI()

router = APIRouter(prefix="/analyze", tags=["analyze"])


def plt_to_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return base64.b64encode(buf.getvalue()).decode("utf-8")


@router.get("/{file_id}")
async def _analyze_file(
    file_id: UUID,
    user_id: UUID = Depends(get_user_id),
):
    response = await analyze_file(f"data/users/{user_id}/{file_id}.parquet")
    return {
        "answer": response[0],
        "files": [{"image_base64": plt_to_base64()} for _ in response[1]],
    }
