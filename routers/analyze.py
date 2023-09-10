"""routers.analyze.py"""

import base64
import io
from uuid import UUID

import matplotlib.pyplot as plt
from fastapi import FastAPI, APIRouter, Depends

from dependencies import get_user_id
from mlbot.agent import analyze_file, analyze_ml_models

app = FastAPI()

router = APIRouter(prefix="/analyze", tags=["analyze"])


def image_data_to_base64(image_data: bytes) -> str:
    return base64.b64encode(image_data).decode("utf-8")


@router.get("/{file_id}")
async def _analyze_file(
    file_id: UUID,
    user_id: UUID = Depends(get_user_id),
):
    response = await analyze_file(f"data/users/{user_id}/{file_id}.parquet")

    # List to store Base64 encoded images
    encoded_images = []

    for file in response.files:
        image_data = (
            file.get_data()
        )  # This assumes that there's a method to get image data in bytes
        encoded_images.append(image_data_to_base64(image_data))

    return {
        "answer": response.content,
        "files": encoded_images,
    }


@router.get("/models/{file_id}")
async def _analyze_ml_models(
    file_id: UUID,
    user_id: UUID = Depends(get_user_id),
):
    responses = await analyze_ml_models(f"data/users/{user_id}/{file_id}.parquet")

    vals = []
    for response in responses:
        # List to store Base64 encoded images
        encoded_images = []
        for file in response.files:
            image_data = file.get_data()
            encoded_images.append(image_data_to_base64(image_data))

        vals.append(
            {
                "answer": response.content,
                "files": encoded_images,
            }
        )

    return vals
