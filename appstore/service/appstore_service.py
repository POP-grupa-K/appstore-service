from sqlalchemy.orm import Session

from appstore.model.appstore_model import AppStore as AppStoreModel
from appstore.schema.appstore_schema import AppStore as AppStoreSchema


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
