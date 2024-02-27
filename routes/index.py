from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Viewing Home Page / Index"}
