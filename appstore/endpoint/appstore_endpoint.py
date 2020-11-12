import sys
import traceback

import str as str
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from appstore.schema.appstore_schema import AppStoreSchema as AppStoreSchema
from appstore.schema.rating_schema import RatingSchema
from appstore.service.appstore_service import create_app, delete_app, update_app, add_app_rate, \
    get_all_as_dict, get_app_schema
from run import SessionLocal
from fastapi.responses import JSONResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", tags=["Backend AppStore"])
async def list_apps(db: Session = Depends(get_db)):
    apps = get_all_as_dict(db)
    if apps is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=apps)

    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/", tags=["Backend AppStore"])
async def add_app(app: AppStoreSchema, db: Session = Depends(get_db)) -> str:
    try:
        app_id = create_app(app, db)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=app_id)

    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=e)


@router.delete("/{id_app}", tags=["Backend AppStore"])
async def remove_app(id_app: int, db: Session = Depends(get_db)):
    try:
        is_deleted = delete_app(id_app, db)
        if is_deleted is not None and is_deleted:
            return JSONResponse(status_code=status.HTTP_200_OK, content=id_app)

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f"App with id = {id_app} was not found.")
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=e)


@router.put("/{id_app}", tags=["Backend AppStore"])
async def put_app(id_app: int, app: AppStoreSchema, db: Session = Depends(get_db)):
    try:
        is_updated = update_app(id_app, app, db)
        if is_updated is not None and is_updated:
            return JSONResponse(status_code=status.HTTP_200_OK, content=id_app)

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f"App with id = {id_app} was not found.")
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=e)


@router.post("/{id_app}/rate", tags=["Backend AppStore"])
async def rate_app(id_app: int, rate: RatingSchema, db: Session = Depends(get_db)):
    res = add_app_rate(id_app, rate, db)
    if res:
        return JSONResponse(status_code=status.HTTP_200_OK, content=res)
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{id_app}", tags=["Backend AppStore"])
async def get_app(id_app: int, db: Session = Depends(get_db)):
    try:
        app: AppStoreSchema = get_app_schema(id_app, db)
        if app is not None:
            return JSONResponse(status_code=status.HTTP_200_OK, content=app.json())

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f"App with id = {id_app} was not found.")
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=e)
