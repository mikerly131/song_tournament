from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from services import auth_svc


templates = Jinja2Templates(directory='templates')
router = APIRouter()


@router.get("/")
async def index(request: Request, user_id: int = Depends(auth_svc.get_user_id_via_auth_cookie)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user_id})
