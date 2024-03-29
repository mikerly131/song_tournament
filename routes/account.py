"""
Has routes for registering an account, logging in, and viewing the account.
Has routes available when viewing the account: my song lists, my brackets, my filled out brackets

User/Account are synonymous in terms of this application - Users are Accounts, not having them
"""
from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from data.database import get_db_session
from services import auth_svc, account_svc

templates = Jinja2Templates(directory='templates')
router = APIRouter()


@router.get("/view/account/")
async def get_account(request: Request, user_id: int = Depends(auth_svc.get_user_id_via_auth_cookie)):
    return {"message": "Viewing Account Page"}


@router.get("/register/account")
async def get_register(request: Request, user_id: int = Depends(auth_svc.get_user_id_via_auth_cookie)):
    return templates.TemplateResponse("register.html", {"request": request, "user_id": user_id})


@router.post("/register/account")
async def register_account(request: Request, db: Session = Depends(get_db_session)):

    form_data = await request.form()
    username = form_data.get('username')
    password = form_data.get('password')

    user = account_svc.create_account(db, username, password)

    resp = RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
    auth_svc.set_auth_cookie(resp, user)

    return resp


@router.get("/login/account")
async def get_login(request: Request, user_id: int = Depends(auth_svc.get_user_id_via_auth_cookie)):
    return templates.TemplateResponse("login.html", {"request": request, "user_id": user_id})


@router.post("/login/account")
async def login_account(request: Request, db: Session = Depends(get_db_session)):

    form_data = await request.form()
    username = form_data.get('username')
    password = form_data.get('password')

    user = account_svc.login_account(db, username, password)
    if not user:
        error = 'Either account does not exist or the password is incorrect.'
        return error

    resp = RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
    auth_svc.set_auth_cookie(resp, user['id'])

    return resp


@router.get("/logout/account")
async def logout_account():
    response = RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
    auth_svc.logout(response)
    return response

# Uncomment below when ready to setup user profile template and routes

# @router.get("/view/account/{user}/my_song_lists")
# async def get_account_song_lists(user: int):
#     song_lists = f"The {user} created song lists"
#     return {"message": song_lists}
#
#
# @router.get("/view/account/{user}/my_tournaments")
# async def get_account_tournaments(user: int):
#     user_brackets = f"The {user} created tournaments"
#     return {"message": user_brackets}
#
#
# @router.get("/view/account/{user}/my_filled_out_brackets")
# async def get_account_ranked_brackets(user: int):
#     user_filled_brackets = f"The brackets the {user} filled out"
#     return {"message": user_filled_brackets}
