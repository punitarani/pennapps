"""routers.upload.py"""

from fastapi import FastAPI, APIRouter

app = FastAPI()

router = APIRouter(prefix="/upload", tags=["upload"])
