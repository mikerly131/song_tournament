"""
Has the routes for registering an account, logging in, and viewing the account's profile

User/Account are synonymous in terms of this application - Users are Accounts, not having them
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/profile")
async def get_profile():
    return {"message": "Viewing a Profile"}
