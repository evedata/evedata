from fastapi import APIRouter

app = APIRouter()


@app.get("/")
def get_root():
    return {}
