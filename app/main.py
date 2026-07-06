from fastapi import FastAPI

from app.api.v1 import auth, department



app = FastAPI(title="FAST API")

app.include_router(auth.router)
app.include_router(department.router)


@app.get("/")
def root():
    return {"status": "ok"}