from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from appstore.schema.appstore import AppStore as AppStoreSchema
from appstore.service.appstore import create_app
from run import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", tags=["Backend AppStore"])
async def list_apps():
    return "Show AppStore"


@router.post("/", tags=["Backend AppStore"])
async def add_app(app: AppStoreSchema, db: Session = Depends(get_db)):
    create_app(app, db)
    return "Add app to AppShelf"


@router.delete("/{app_uid}/remove", tags=["Backend AppStore"])
async def remove_app(app_uid: str):
    return "Remove app from AppShelf"


@router.put("/{app_uid}", response_model=AppStoreSchema, tags=["Backend AppStore"])
async def update_app(app_uid: str, app: AppStoreSchema):
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
