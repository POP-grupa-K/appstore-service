from fastapi import APIRouter

router = APIRouter()


@router.get("/example1")
async def example1():
    return "example1"
