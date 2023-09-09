"""routers.chat.py"""

from fastapi import FastAPI, APIRouter

app = FastAPI()

router = APIRouter(prefix="/chat", tags=["chat"])
