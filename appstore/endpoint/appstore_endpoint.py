import sys
import traceback
import io

import str as str
from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from appstore.exceptions.appstore_exceptions import UnsupportedMediaTypeException, InvalidFileNameException, \
    ImageAlreadyExistsException, NoSuchAppException, NoSuchImageException, AppNameExists, NoSuchRatingException
from appstore.schema.appstore_schema import AppStoreSchema as AppStoreSchema
from appstore.schema.rating_schema import RatingSchema
from appstore.service.appstore_service import create_app, delete_app, update_app, add_app_rate_and_update_average, \
    get_all_apps_as_json_list, get_app_schema, save_image, get_image, delete_image, update_image, \
    get_ratings_as_json_list, delete_rating, update_rating_and_average
from appstore.utils.message_encoder.json_message_encoder import encode_to_json_message
from appstore.utils.validator.file_validator import validate_image
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
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=encode_to_json_message(app_id))

    except AppNameExists as e:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=encode_to_json_message(f"App with name {app.name_app} exists"))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=encode_to_json_message(e))


@router.delete("/{id_app}", tags=["Backend AppStore"])
async def remove_app(id_app: int, db: Session = Depends(get_db)):
    try:
        is_deleted = delete_app(id_app, db)
        if is_deleted is not None and is_deleted:
            return JSONResponse(status_code=status.HTTP_200_OK, content=encode_to_json_message(id_app))

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=encode_to_json_message(f"App with id = {id_app} was not found."))
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=encode_to_json_message(e))


@router.put("/{id_app}", tags=["Backend AppStore"])
async def put_app(id_app: int, app: AppStoreSchema, db: Session = Depends(get_db)):
    try:
        is_updated = update_app(id_app, app, db)
        if is_updated is not None and is_updated:
            return JSONResponse(status_code=status.HTTP_200_OK, content=encode_to_json_message(id_app))

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=encode_to_json_message(f"App with id = {id_app} was not found."))
    except AppNameExists as e:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=encode_to_json_message(f"App with name {app.name_app} exists"))
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=encode_to_json_message(e))


@router.post("/{id_app}/rate", tags=["Backend AppStore"])
async def rate_app(id_app: int, rate: RatingSchema, db: Session = Depends(get_db)):
    res = add_app_rate_and_update_average(id_app, rate, db)
    if res:
        return JSONResponse(status_code=status.HTTP_200_OK, content=encode_to_json_message(res))
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{id_app}", tags=["Backend AppStore"])
async def get_app(id_app: int, db: Session = Depends(get_db)):
    try:
        app: AppStoreSchema = get_app_schema(id_app, db)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(app))
    except NoSuchAppException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=encode_to_json_message(f"No application with id = {id_app}"))
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=encode_to_json_message(e))


@router.post("/img/{id_app}", tags=["Backend AppStore"])
async def upload_app_img(id_app: int, db: Session = Depends(get_db), image: UploadFile = File(...)):
    try:
        validate_image(image)
        save_image(id_app, image, db)
        return JSONResponse(status_code=status.HTTP_200_OK, content=encode_to_json_message("OK"))

    except InvalidFileNameException:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=encode_to_json_message("Bad filename. Expected JPG or PNG."))
    except NoSuchAppException:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            content=encode_to_json_message(f"App with id = {id_app} was not found."))
    except ImageAlreadyExistsException:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=encode_to_json_message("Image already exists."))
    except UnsupportedMediaTypeException:
        return JSONResponse(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/img/{id_app}", tags=["Backend AppStore"])
async def update_app_img(id_app: int, db: Session = Depends(get_db), image: UploadFile = File(...)):
    try:
        validate_image(image)
        update_image(id_app, image, db)
        return JSONResponse(status_code=status.HTTP_200_OK, content=encode_to_json_message("OK"))

    except InvalidFileNameException:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=encode_to_json_message("Bad filename. Expected JPG or PNG."))
    except NoSuchAppException:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            content=encode_to_json_message(f"App with id = {id_app} was not found."))
    except ImageAlreadyExistsException:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=encode_to_json_message("Image already exists."))
    except UnsupportedMediaTypeException:
        return JSONResponse(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/img/{id_app}", tags=["Backend AppStore"])
async def get_app_img(id_app: int, db: Session = Depends(get_db)):
    try:
        img_model = get_image(id_app, db)
        if img_model is not None:
            file = io.BytesIO(img_model.img)

            if img_model.filename.lower().endswith(".jpg"):
                return StreamingResponse(file, media_type="image/jpeg")
            elif img_model.filename.lower().endswith(".png"):
                return StreamingResponse(file, media_type="image/png")
            else:
                raise Exception("illegal state of img model")

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=encode_to_json_message("No such image"))
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/img/{id_app}", tags=["Backend AppStore"])
async def delete_app_img(id_app: int, db: Session = Depends(get_db)):
    try:
        delete_image(id_app, db)
        return JSONResponse(status_code=status.HTTP_200_OK, content=encode_to_json_message("OK"))

    except NoSuchImageException:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=encode_to_json_message("No such image."))
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Rating
@router.get("/rating/{app_uid}", tags=["AppStore Ratings"])
async def get_ratings(app_uid: int, db: Session = Depends(get_db)):
    ratings = get_ratings_as_json_list(app_uid, db)
    if ratings is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(ratings))

    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/rating/{rating_id}", tags=["AppStore Ratings"])
async def delete_rating_by_id(rating_id: int, db: Session = Depends(get_db)):
    try:
        delete_rating(rating_id, db)
        return JSONResponse(status_code=status.HTTP_200_OK, content=encode_to_json_message("OK"))

    except NoSuchRatingException:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=encode_to_json_message("No such rating."))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/rating/{rating_id}", tags=["AppStore Ratings"])
async def put_rating(rating_id: int, rating: RatingSchema, db: Session = Depends(get_db)):
    try:
        is_updated = update_rating_and_average(rating_id, rating, db)
        if is_updated is not None and is_updated:
            return JSONResponse(status_code=status.HTTP_200_OK, content=encode_to_json_message(rating_id))

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=encode_to_json_message(f"Rating with id = {rating_id} was not found."))
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=encode_to_json_message(e))
