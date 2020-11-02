from appstore.model.appstore import AppStore as AppStoreModel
from appstore.schema.appstore import AppStore as AppStoreSchema


def create_app(app: AppStoreSchema, db):
    new_app = AppStoreModel(name_app=app.name_app, ranking=app.ranking, date_update=app.date_update, description_app=app.description_app)
    #TODO trzeba zmienic tak, aby podawac tylko obiekt klasy AppStoreSchema, a nie przepisywac po kolei kazda wartosc. Mozna przez classmethod
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
