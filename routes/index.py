from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory='templates')
router = APIRouter()


@router.get("/")
async def index(request: Request, is_authenticated: bool = False):
    mock_user = {"username": "Testboi", "is_authenticated": is_authenticated}
    response_context = {"request": request, "user": mock_user}
    return templates.TemplateResponse("index.html", response_context)
