from importlib import metadata

import typer
from evedata_platform_admin_core import AdminState
from typer import Typer

from evedata_platform_admin._api import cli as api_cli

from . import _commands as commands

app = Typer(name="evedata")

entrypoints = metadata.entry_points(group="evedata.admin.commands")
for entrypoint in entrypoints:
    command_app = entrypoint.load()
    app.add_typer(command_app, name=entrypoint.name)

app.add_typer(api_cli, name="admin-api")

app.add_typer(commands.config_cmd, name="config")


@app.callback()
def callback(ctx: typer.Context):
    """EVEData Admin CLI."""
    ctx.ensure_object(AdminState)
