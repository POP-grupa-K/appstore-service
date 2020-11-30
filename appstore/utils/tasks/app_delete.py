from fastapi import APIRouter
from fastapi_utils.tasks import repeat_every

router = APIRouter()


@router.on_event('startup')
@repeat_every(seconds=1)
async def remove_waiting_apps() -> None:
    print("foo")
