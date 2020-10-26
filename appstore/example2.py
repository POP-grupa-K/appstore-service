from fastapi import APIRouter

router = APIRouter()


@router.get("/example2")
async def example2():
    return "example2"
