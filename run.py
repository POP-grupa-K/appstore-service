import uvicorn as uvicorn
from fastapi import FastAPI

from appstore import app_store, rating_manager


app = FastAPI()


if __name__ == "__main__":
    app.include_router(app_store.router)
    app.include_router(rating_manager.router)
    uvicorn.run(app, host="0.0.0.0", port=8005)
