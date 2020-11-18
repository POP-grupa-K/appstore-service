from appstore.model.rating_model import RatingModel
from appstore.schema.rating_schema import RatingSchema


def rating_model_to_schema(rating_model: RatingModel) -> RatingSchema:
    return RatingSchema(
        id_rating=rating_model.id_rating,
        value=rating_model.value,
        id_app=rating_model.id_app,
        comm=rating_model.comm,
        date_update=rating_model.date_update,
        id_user=rating_model.id_user
    )
