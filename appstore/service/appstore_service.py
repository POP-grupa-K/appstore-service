from sqlalchemy.orm import Session

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


def update_app(id_app: int, app_model: AppStoreModel, db: Session) -> bool:
    app = get_app_by_id(id_app, db)
    app.name_app = app_model.name_app
    app.date_update = app_model.date_update
    app.description_app = app_model.description_app
    app.ranking = app_model.ranking

    db.add(app_model)
    db.commit()
    db.refresh(app_model)
    return True

