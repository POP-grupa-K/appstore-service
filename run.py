import os
import uvicorn as uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from appstore.endpoint import appstore_endpoint

app = FastAPI(title="System obliczeń wysokoskalowych")

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

if __name__ == "__main__":
    app.include_router(appstore_endpoint.router, prefix="/appstore")

    uvicorn.run(app, host="0.0.0.0", port=8005)

