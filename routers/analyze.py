"""routers.analyze.py"""

import base64
from uuid import UUID

from fastapi import APIRouter, Body, Depends

from dependencies import get_user_id
from mlbot.agent import analyze_file, analyze_ml_models, df_query

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


@router.post("/df-query/{file_id}")
async def _df_query(
    file_id: UUID,
    query: str = Body(
        ..., description="The pandas query to be executed on the dataframe."
    ),
    user_id: UUID = Depends(get_user_id),
):
    response = await df_query(f"data/users/{user_id}/{file_id}.parquet", query)
    return {"answer": response}
