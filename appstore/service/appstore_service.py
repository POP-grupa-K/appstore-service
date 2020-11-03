from sqlalchemy.orm import Session
from typing import List

from appstore.model.appstore_model import AppStoreModel
from appstore.schema.appstore_schema import AppStoreSchema


def create_app(app: AppStoreSchema, db: Session) -> int:
    new_app = AppStoreModel.from_schema(app)

    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app.id_app


def delete_app(id_app: int, db: Session) -> bool:
    app = get_app_by_id(id_app, db)
    if app is None:
        return False

    db.delete(app)
    db.commit()
    return True


def get_app_by_id(id_app: int, db: Session) -> AppStoreModel:
    return db.query(AppStoreModel).filter(AppStoreModel.id_app == id_app).first()


def update_app(app_id: int, updated_app: AppStoreSchema, db: Session) -> bool:
    app = get_app_by_id(app_id, db)

    app.name_app = updated_app.name_app
    app.date_update = updated_app.date_update
    app.description_app = updated_app.description_app
    app.ranking = updated_app.ranking

    db.commit()
    return True


def rate_app(app_id: int, rate: int) -> bool:
    app = get_app_by_id(app_id, db)

    app.ranking = rate

    db.commit()
    return True


def get_all(db: Session) -> List[AppStoreSchema]:
    app_models = db.query(AppStoreModel).all()
    # TODO MAP AppStoreModels to AppStoreSchemas
    return app_models
