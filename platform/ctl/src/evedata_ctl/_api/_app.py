from importlib import metadata

from fastapi import FastAPI

app = FastAPI()

entrypoints = metadata.entry_points(group="evedata_ctl.endpoints")
for entrypoint in entrypoints:
    router = entrypoint.load()
    app.include_router(router, prefix=f"/{entrypoint.name}")


@app.get("/")
def get_root():
    return {}
