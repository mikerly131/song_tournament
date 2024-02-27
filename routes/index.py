from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory='templates')
router = APIRouter()


@router.get("/")
async def index(request: Request):
    mock_user = {"username": "Testboi", "is_authenticated": False}
    response_context = {"request": request, "user": mock_user}
    return templates.TemplateResponse("index.html", response_context)
