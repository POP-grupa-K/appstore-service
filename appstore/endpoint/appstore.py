from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from appstore.schema.appstore import AppStore as AppStoreSchema
from appstore.service.appstore import create_app, delete_app, get_app_by_id
from run import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#TODO
@router.get("/", tags=["Backend AppStore"])
async def list_apps():
    return "Show AppStore"


@router.post("/", tags=["Backend AppStore"])
async def add_app(app: AppStoreSchema, db: Session = Depends(get_db)) -> str:
    app_id = create_app(app, db)
    return f"Application created. Id = {app_id}"


@router.delete("/{id_app}", tags=["Backend AppStore"])
async def remove_app(id_app: int, db: Session = Depends(get_db)):
    if delete_app(id_app, db):
        return "App deleted"
    return "App not found"

#TODO
@router.put("/{id_app}", response_model=AppStoreSchema, tags=["Backend AppStore"])
async def update_app(id_app: str, app: AppStoreSchema):
    # ...
    updated_app = app
    # ...
    return updated_app


#TODO
@router.post("/{id_app}/rate", tags=["Backend AppStore"])
async def rate_app(id_app: str):
    return "Rate app"


@router.get("/{id_app}", tags=["Backend AppStore"])
async def get_app(id_app: int, db: Session = Depends(get_db)):
    app = get_app_by_id(id_app, db)
    if app is not None:
        return app
    return "App not found"
