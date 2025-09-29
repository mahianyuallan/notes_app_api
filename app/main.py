from fastapi import FastAPI
from . import models
from .database import engine
from .routes import users, notes

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes App")

# Routes
app.include_router(users.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "Welcome to Notes App Backend 🚀"}
