import uvicorn as uvicorn
from fastapi import FastAPI
from appstore import example1, example2

app = FastAPI()

if __name__ == "__main__":
    app.include_router(example1.router)
    app.include_router(example2.router)
    uvicorn.run(app, host="0.0.0.0", port=8005, reload=True)
    pass
