"""
Has routes for creating, viewing and filling out brackets
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/brackets")
async def get_bracket_home():
    return {"message": "Viewing Bracket Home"}