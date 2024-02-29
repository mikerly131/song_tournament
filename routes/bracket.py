"""
Has routes for creating, viewing and filling out brackets
"""
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')
router = APIRouter()


@router.get("/brackets/create")
async def get_bracket(request: Request, is_authenticated: bool = False):
    mock_user = {"username": "Testboi", "is_authenticated": is_authenticated}
    return templates.TemplateResponse("/brackets/create-bracket.html", {"request": request, "user": mock_user})


@router.post("/brackets/create")
async def create_bracket():
    # response_template = f"view-bracket-{bracket_size}.html"
    return {"message": "Viewing Bracket Home"}


@router.get("/brackets/fill-out")
async def fill_out_bracket(request: Request):
    return templates.TemplateResponse("/brackets/view-bracket-8.html", {"request": request})
