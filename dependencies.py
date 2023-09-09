"""
dependencies.py

FastAPI dependencies
"""

from uuid import UUID

from fastapi import Header, HTTPException


async def get_user_id(user_id: UUID = Header()) -> UUID:
    """
    A dependency to ensure user_id is provided
    """
    if user_id is None:
        raise HTTPException(status_code=400, detail="user_id header is required")
    return user_id
