from importlib import metadata
from typing import Any

from fastapi import FastAPI

app = FastAPI()

entrypoints = metadata.entry_points(group="evedata.admin.endpoints")
for entrypoint in entrypoints:
    router = entrypoint.load()
    app.include_router(router, prefix=f"/{entrypoint.name}")


@app.get("/")
def get_root() -> dict[str, Any]:
    return {}
