from fastapi import FastAPI

app = FastAPI(
    title="Fast API Application"
)

@app.get("/")
def home():
    return {
        "message":"Hi"
    }