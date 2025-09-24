from fastapi import FastAPI
from . import models
from .database import engine

# Create tables
models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Notes App")

@app.get("/")
def root():
    return {"message": "Welcome to Notes App Backend 🚀"}
