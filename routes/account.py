"""
Has routes for registering an account, logging in, and viewing the account.
Has routes available when viewing the account: my song lists, my brackets, my filled out brackets

User/Account are synonymous in terms of this application - Users are Accounts, not having them
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/account")
async def get_account():
    return {"message": "Viewing Account Page"}


@router.get("/account/register")
async def register_get():
    return {"message": "Viewing Register Account Page"}


@router.post("/account/register")
async def register_post():
    return {"message": "Post to register account, will re-direct to login."}


@router.get("/account/login")
async def login_get():
    return {"message": "Viewing Login Account Page"}


@router.post("/account/login")
async def login_post():
    return {"message": "Post of login account, will re-direct to login."}

# Uncomment below when ready to setup user profile template and routes

# @router.get("/account/{user}/my_song_lists")
# async def get_account_song_lists(user: int):
#     song_lists = f"The {user} created song lists"
#     return {"message": song_lists}
#
#
# @router.get("/account/{user}/my_created_brackets")
# async def get_account_brackets(user: int):
#     user_brackets = f"The {user} created brackets"
#     return {"message": user_brackets}
#
#
# @router.get("/account/{user}/my_filled_out_brackets")
# async def get_account_ranked_brackets(user: int):
#     user_filled_brackets = f"The brackets the {user} filled out"
#     return {"message": user_filled_brackets}
