from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from run import db



router = APIRouter()


class AppStore(BaseModel):
    idapp: Optional[str] = None
    name_app: Optional[str]
    ranking: Optional[str] = None
    date_update: Optional[datetime] = None
    description_app: Optional[str] = None


@router.get("/", tags=["Backend AppStore"])
async def list_apps():
    test = AppStore(name_app="test")
    db.add(test)
    return "Show AppStore"


@router.post("/add", tags=["Backend AppStore"])
async def add_app():
    return "Add app to AppShelf"


@router.delete("/{app_uid}/remove", tags=["Backend AppStore"])
async def remove_app(app_uid: str):
    return "Remove app from AppShelf"


@router.put("/{app_uid}", response_model=AppStore, tags=["Backend AppStore"])
async def update_app(app_uid: str, app: AppStore):
    # ...
    updated_app = app
    # ...
    return updated_app


@router.post("/{app_uid}/rate", tags=["Backend AppStore"])
async def rate_app(app_uid: str):
    return "Rate app"


@router.get("/{app_uid}", tags=["Backend AppStore"])
async def app_details(app_uid: str):
    return "App details"
