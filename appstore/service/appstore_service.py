from sqlalchemy.orm import Session
from typing import List

from appstore.model.appstore_model import AppStoreModel
from appstore.schema.appstore_schema import AppStoreSchema
from appstore.model.rating_model import RatingModel
from appstore.schema.rating_schema import RatingSchema
from appstore.utils.mapper.appstore_mapper import appstore_model_to_schema


def create_app(app: AppStoreSchema, db: Session) -> int:
    new_app = AppStoreModel.from_schema(app)

    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app.id_app


def get_all(db: Session) -> List[AppStoreModel]:
    app_models = db.query(AppStoreModel).all()
    return app_models


def get_all_as_dict(db: Session):
    app_models = get_all(db)

    apps = []
    for app in app_models:
        apps.append(None)
    return apps


def get_app_model(id_app: int, db: Session):
    return db.query(AppStoreModel).filter(AppStoreModel.id_app == id_app).first()


def get_app_schema(id_app: int, db: Session):
    app_model = get_app_model(id_app, db)
    return appstore_model_to_schema(app_model)


def delete_app(id_app: int, db: Session) -> bool:
    app = get_app_model(id_app, db)
    if app is None:
        return False

    db.delete(app)
    db.commit()
    return True


def update_app(app_id: int, updated_app: AppStoreSchema, db: Session) -> bool:
    app = get_app_model(app_id, db)
    if app is None:
        return False

    app.name_app = updated_app.name_app
    app.date_update = updated_app.date_update
    app.description_app = updated_app.description_app
    app.ranking = updated_app.ranking

    db.commit()
    return True


def add_app_rate(app_id: int, rate: RatingSchema, db: Session) -> int:
    new_rate = RatingModel.from_schema(rate)

    db.add(new_rate)
    db.commit()
    db.refresh(new_rate)

    db.commit()
    return new_rate.id_rating