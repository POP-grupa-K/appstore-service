import uvicorn as uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from appstore.endpoint import appstore_endpoint

app = FastAPI(title="System obliczeń wysokoskalowych")

origins = [
    "*"
]


if __name__ == "__main__":
    app.include_router(appstore_endpoint.router, prefix="/appstore")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    uvicorn.run(app, host="0.0.0.0", port=8005)
