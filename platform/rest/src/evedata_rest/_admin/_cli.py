from typing import Annotated

import typer
from typer import Typer

cli = Typer(name="evedata-rest-api")


def _run(*, host: str, port: int, log_level: str, reload: bool) -> None:
    import uvicorn  # noqa: PLC0415

    config = uvicorn.Config(
        "evedata_rest_api._app:app",
        host=host,
        port=port,
        log_level=log_level,
        proxy_headers=True,
        reload=reload,
    )
    server = uvicorn.Server(config)
    server.run()


@cli.callback()
def callback() -> None:
    """Manage the REST API."""


@cli.command(name="dev")
def dev_cmd(
    *,
    host: Annotated[
        str, typer.Option(help="The host to bind the server to.")
    ] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="The port to bind the server to.")] = 5000,
    log_level: Annotated[str, typer.Option(help="The log level to use.")] = "info",
):
    """Start the REST API in dev mode."""
    _run(host=host, port=port, log_level=log_level, reload=True)


@cli.command(name="start")
def start_cmd(
    *,
    host: Annotated[
        str, typer.Option(help="The host to bind the server to.")
    ] = "0.0.0.0",  # noqa: S104
    port: Annotated[int, typer.Option(help="The port to bind the server to.")] = 5000,
    log_level: Annotated[str, typer.Option(help="The log level to use.")] = "info",
    reload: Annotated[bool, typer.Option(help="Enable auto-reload.")] = False,
):
    """Start the REST API."""
    _run(host=host, port=port, log_level=log_level, reload=reload)
