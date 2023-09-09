"""routers.chat.py"""

from uuid import UUID

from fastapi import FastAPI, APIRouter, Body, Depends
from pydantic import BaseModel

from dependencies import get_user_id
from mlbot.models import FileType

app = FastAPI()

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    file_id: UUID
    file_type: FileType
    query: str


@router.post("/")
async def get_response(
    request: ChatRequest = Body(...),
    user_id: UUID = Depends(get_user_id),
):
    return {
        "answer": request.query,
    }
