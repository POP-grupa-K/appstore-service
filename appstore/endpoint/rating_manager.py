from typing import Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.encoders import jsonable_encoder

from appstore.endpoint.appstore_endpoint import get_db
from appstore.schema.rating_schema import RatingSchema
from appstore.service.appstore_service import get_ratings_as_json_list

router = APIRouter()


class RatingItem(BaseModel):
    user: Optional[str] = None
    rating: Optional[int] = None


@router.get("/{app_uid}", tags=["AppStore Ratings"])
async def get_ratings(app_uid: str, db: Session = Depends(get_db)):
    ratings = get_ratings_as_json_list(app_uid, db)
    if ratings is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(ratings))

    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

#
# @router.post("/{app_uid}", tags=["AppStore Ratings"])
# async def rate_app(
#     app_uid: str,
#     user: str,
#     rating: int = Query(5, title="App rating", gt=0, lte=5)
# ):
#     return "Rate App"
#
#
# @router.put("/{app_uid}", response_model=RatingItem, tags=["AppStore Ratings"])
# async def update_rating(app_uid: str, rating: RatingItem):
#     # ...
#     updated_rating = rating
#     # ...
#     return updated_rating
#
#
# @router.delete("/{app_uid}", tags=["AppStore Ratings"])
# async def delete_rating(
#     app_uid: str,
#     user: str
# ):
#     return "Delete Rating"
