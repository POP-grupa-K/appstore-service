from typing import Dict

from appstore.model.appstore_model import AppStoreModel
from appstore.schema.appstore_schema import AppStoreSchema


def appstore_model_to_schema(app_model: AppStoreModel) -> AppStoreSchema:
    return AppStoreSchema(
        id_app=app_model.id_app,
        name_app=app_model.name_app,
        ranking=app_model.ranking,
        date_update=app_model.date_update,
        description_app=app_model.description_app
    )


def appstore_model_to_dict(app_model: AppStoreModel):
    if app_model is None:
        return None

    return {
        "idApp": app_model.id_app,
        "nameApp": app_model.name_app,
        "ranking": app_model.ranking,
        "dateUpdate": app_model.date_update,
        "descriptionApp": app_model.description_app
    }
