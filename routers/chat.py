"""routers.chat.py"""

from uuid import UUID

from fastapi import FastAPI, APIRouter, Body, Depends
from pydantic import BaseModel

from dependencies import get_user_id
from mlbot.agent import chat

app = FastAPI()

router = APIRouter(prefix="/chat", tags=["chat"])


@app.get("/{file_id}")
async def _chat(
    file_id: UUID,
    query: str = Body(..., description="User's query to be answered by the AI agent."),
    user_id: UUID = Depends(get_user_id),
):
    response = await chat(f"data/users/{user_id}/{file_id}.parquet", query)
    return {"answer": response}
