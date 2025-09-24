from fastapi import FastAPI

app = FastAPI(title="Notes App")

@app.get("/")
def root():
    return {"message": "Welcome to Notes App Backend 🚀"}
