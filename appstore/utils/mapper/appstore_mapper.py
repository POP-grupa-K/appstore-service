from appstore.model.appstore_model import AppStoreModel
from appstore.schema.appstore_schema import AppStoreSchema


def appstore_model_to_schema(app_model: AppStoreModel) -> AppStoreSchema:
    return AppStoreSchema(
        id_app=app_model.id_app,
        name_app=app_model.name_app,
        ranking=app_model.ranking,
        date_update=app_model.date_update,
        description_app=app_model.description_app,
        times_used=app_model.times_used,
        status=app_model.status,
        id_user=app_model.id_user
    )
