from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel


router = APIRouter()


class RatingItem(BaseModel):
    user: Optional[str] = None
    rating: Optional[int] = None


@router.get("/{app_uid}", tags=["AppStore Ratings"])
async def get_rating(
    app_uid: str,
    user: str
):
    return "Get Rating"


@router.post("/{app_uid}", tags=["AppStore Ratings"])
async def rate_app(
    app_uid: str,
    user: str,
    rating: int = Query(5, title="App rating", gt=0, lte=5)
):
    return "Rate App"


@router.put("/{app_uid}", response_model=RatingItem, tags=["AppStore Ratings"])
async def update_rating(app_uid: str, rating: RatingItem):
    # ...
    updated_rating = rating
    # ...
    return updated_rating


@router.delete("/{app_uid}", tags=["AppStore Ratings"])
async def delete_rating(
    app_uid: str,
    user: str
):
    return "Delete Rating"
