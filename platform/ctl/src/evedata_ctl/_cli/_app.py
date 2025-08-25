from importlib import metadata

from typer import Typer

from evedata_ctl._api import cli as api_cli

app = Typer(name="evedata")

entrypoints = metadata.entry_points(group="evedata_ctl.commands")
for entrypoint in entrypoints:
    command_app = entrypoint.load()
    app.add_typer(command_app, name=entrypoint.name)

app.add_typer(api_cli, name="ctl-api")


@app.callback(invoke_without_command=True, no_args_is_help=True)
def callback():
    """EVEData Control CLI."""
