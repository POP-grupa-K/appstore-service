from datetime import datetime

from fastapi import UploadFile
from sqlalchemy.orm import Session
from typing import List

from appstore.exceptions.appstore_exceptions import ImageAlreadyExistsException, NoSuchAppException, \
    NoSuchImageException, AppNameExists, NoSuchRatingException
from appstore.model.appstore_model import AppStoreModel
from appstore.model.image_model import ImageModel
from appstore.schema.appstore_schema import AppStoreSchema
from appstore.model.rating_model import RatingModel
from appstore.schema.rating_schema import RatingSchema
from appstore.utils.mapper.appstore_mapper import appstore_model_to_schema
from appstore.utils.mapper.rating_mapper import rating_model_to_schema


def create_app(app: AppStoreSchema, db: Session) -> int:
    new_app = AppStoreModel.from_schema(app)
    if get_app_model_by_name(new_app.name_app, db):
        raise AppNameExists(f"App with name {new_app.name_app} exists")
    new_app.date_update = datetime.now().isoformat()

    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app.id_app


def get_all_apps(db: Session) -> List[AppStoreModel]:
    app_models = db.query(AppStoreModel).all()
    return app_models


def get_all_apps_as_json_list(db: Session):
    app_models = get_all_apps(db)

    apps = []
    for app in app_models:
        apps.append(appstore_model_to_schema(app).json())
    return apps


def get_app_model_by_name(name: str, db: Session):
    app = db.query(AppStoreModel).filter(AppStoreModel.name_app == name)
    if app.first():
        return app.first()
    return None


def get_app_model(id_app: int, db: Session):
    app = db.query(AppStoreModel).filter(AppStoreModel.id_app == id_app)
    if app.first():
        return app.first()
    return None


def get_app_schema(id_app: int, db: Session):
    app_model = get_app_model(id_app, db)
    if app_model:
        return appstore_model_to_schema(app_model)
    raise NoSuchAppException(f"No application with id = {id_app}")


def delete_app(id_app: int, db: Session) -> bool:
    app = get_app_model(id_app, db)
    if app is None:
        return False

    app.status = 'deleted'

    db.commit()
    return True


def update_app(app_id: int, updated_app: AppStoreSchema, db: Session) -> bool:
    app: AppStoreModel = get_app_model(app_id, db)
    if app is None:
        return False
    app_name_check: AppStoreModel = get_app_model_by_name(updated_app.name_app, db)

    if app_name_check is not None and app_name_check.id_app != app.id_app:
        raise AppNameExists(f"App with name {updated_app.name_app} exists")

    app.name_app = updated_app.name_app
    app.date_update = datetime.now().isoformat()
    app.description_app = updated_app.description_app
    app.ranking = updated_app.ranking

    db.commit()
    return True


def get_app_rates_by_id(app_id: int, db: Session):
    rating_models = db.query(RatingModel).filter(RatingModel.id_app == app_id)
    return rating_models


def add_app_rate(app_id: int, rate: RatingSchema, db: Session) -> bool:
    rate.id_app = app_id
    new_rate = RatingModel.from_schema(rate)
    new_rate.date_update = datetime.now().isoformat()
    db.add(new_rate)
    db.commit()

    return True


def add_app_rate_and_update_average(app_id: int, rate: RatingSchema, db: Session) -> int:
    add_app_rate(app_id, rate, db)
    rating_models = get_app_rates_by_id(app_id, db)
    average = 0.0
    for rating in rating_models:
        average += rating.value
    average /= rating_models.count()
    app: AppStoreModel = get_app_model(app_id, db)
    app.ranking = average
    db.commit()

    return average


def save_image(app_id: int, image: UploadFile, db: Session):
    # check if image already exists
    if get_image(app_id, db) is not None:
        raise ImageAlreadyExistsException

    # check if app exists
    if get_app_model(app_id, db) is None:
        raise NoSuchAppException

    # Cut filename because DB accepts only 50 characters
    cut_filename = image.filename[len(image.filename) - 50:]

    new_img = ImageModel(image.file.read(), cut_filename, app_id)
    db.add(new_img)
    db.commit()
    return True


def update_image(app_id: int, image: UploadFile, db: Session):
    # check if exists
    img = get_image(app_id, db)
    if img is None:
        raise NoSuchImageException

    # delete old one
    db.delete(img)
    db.commit()

    # create a new one
    save_image(app_id, image, db)
    db.commit()


def get_image(app_id: int, db: Session) -> ImageModel:
    image = db.query(ImageModel).filter(ImageModel.id_app == app_id)
    if image is not None:
        return image.first()
    return image


def get_rating(rating_id: int, db: Session) -> RatingModel:
    rating = db.query(RatingModel).filter(RatingModel.id_rating == rating_id)
    if rating is not None:
        return rating.first()
    return rating


def delete_image(app_id: int, db: Session):
    # check if image already exists
    img = get_image(app_id, db)
    if img is None:
        raise NoSuchImageException

    db.delete(img)
    db.commit()


def delete_rating(rating_id: int, db: Session):
    # check if rating already exists
    rating = get_rating(rating_id, db)
    if rating is None:
        raise NoSuchRatingException

    db.delete(rating)
    db.commit()
    
    update_average(rating.id_app, db)


# Rating
def get_ratings(app_uid: int, db: Session) -> List[RatingModel]:
    rating_models = db.query(RatingModel).filter(RatingModel.id_app == app_uid)
    return rating_models


def get_ratings_as_json_list(app_uid: int, db: Session):
    rating_models = get_ratings(app_uid, db)

    ratings = []
    for rating in rating_models:
        ratings.append(rating_model_to_schema(rating).json())
    return ratings


def update_rating_and_average(rating_id: int, updated_rating: RatingSchema, db: Session) -> bool:
    rating: RatingModel = get_rating(rating_id, db)
    if rating is None:
        return False

    # old_id = rating.id_app

    rating.date_update = datetime.now().isoformat()
    rating.value = updated_rating.value
    rating.comm = updated_rating.comm

    update_average(rating.id_app, db)

    # if old_id != rating.id_app:
    #     update_average(old_id, db)

    db.commit()
    return True


def update_average(app_id: int, db: Session):
    rating_models = get_app_rates_by_id(app_id, db)
    average = 0.0
    if rating_models.count() != 0:
        for rating in rating_models:
            average += rating.value
        average /= rating_models.count()
    app: AppStoreModel = get_app_model(app_id, db)
    app.ranking = average

    db.commit()
