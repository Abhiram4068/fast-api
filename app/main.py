from fastapi import FastAPI

from app.api.v1 import auth



app = FastAPI(title="FAST API")

app.include_router(auth.router)


@app.get("/")
def root():
    return {"status": "ok"}