import sys
import traceback
import io

import str as str
from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from appstore.exceptions.appstore_exceptions import UnsupportedMediaType
from appstore.schema.appstore_schema import AppStoreSchema as AppStoreSchema
from appstore.schema.rating_schema import RatingSchema
from appstore.service.appstore_service import create_app, delete_app, update_app, add_app_rate, \
    get_all_apps_as_json_list, get_app_json, save_app_image, get_app_image
from appstore.utils.validator.file_validator import file_is_valid
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
    apps = get_all_apps_as_json_list(db)
    if apps is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(apps))

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
        app: AppStoreSchema = get_app_json(id_app, db)
        if app is not None:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(app))

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f"App with id = {id_app} was not found.")
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=e)


@router.post("/img/{id_app}", tags=["Backend AppStore"])
async def upload_app_img(id_app: int, db: Session = Depends(get_db), image: UploadFile = File(...)):
    try:
        if file_is_valid(image) and save_app_image(id_app, image, db):
            return JSONResponse(status_code=status.HTTP_200_OK, content="OK")

        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    except UnsupportedMediaType:
        return JSONResponse(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/img/{id_app}", tags=["Backend AppStore"])
async def get_app_img(id_app: int, db: Session = Depends(get_db)):
    try:
        img = get_app_image(id_app, db)
        if img is not None:
            file = io.BytesIO(img.img)
            return StreamingResponse(file, media_type="image/jpg")

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f"App with id = {id_app} was not found.")
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
