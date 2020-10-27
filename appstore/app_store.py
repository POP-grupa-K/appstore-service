from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class AppItem(BaseModel):
    uid: Optional[str] = None
    name: Optional[str] = None
    img: Optional[str] = None
    user: Optional[str] = None
    state: Optional[str] = None
    tasks: List[str] = []
    ratings: List[str] = []


@router.get("/appstore")
async def app_details():
    return "Show AppStore"


@router.post("/app/add")
async def add_app():
    return "Add app to AppShelf"


@router.delete("/app/{app_uid}/remove")
async def remove_app(app_uid: str):
    return "Remove app from AppShelf"


@router.put("/app/{app_uid}", response_model=AppItem)
async def update_app(app_uid: str, app: AppItem):
    # ...
    updated_app = app
    # ...
    return updated_app


@router.post("/app/{app_uid}/rate")
async def rate_app(app_uid: str):
    return "Rate app"


@router.get("/app/{app_uid}")
async def app_details(app_uid: str):
    return "App details"
