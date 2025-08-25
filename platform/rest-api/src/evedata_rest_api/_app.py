from importlib import metadata

from fastapi import FastAPI

app = FastAPI()

entrypoints = metadata.entry_points(group="evedata_rest_api.routers")
for entrypoint in entrypoints:
    router = entrypoint.load()
    app.include_router(router, prefix=entrypoint.name)


@app.get("/")
def get_root():
    return {}
