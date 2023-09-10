"""routers.chat.py"""

from uuid import UUID

from fastapi import FastAPI, APIRouter, Body, Depends
from pydantic import BaseModel

from dependencies import get_user_id

app = FastAPI()

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    file_id: UUID
    query: str


@router.post("/")
async def get_response(
    request: ChatRequest = Body(...),
    user_id: UUID = Depends(get_user_id),
):
    return {"answer": str(user_id)}
