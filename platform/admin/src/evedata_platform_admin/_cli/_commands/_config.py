from typing import TYPE_CHECKING

import typer

if TYPE_CHECKING:
    from evedata_platform_admin_core import AdminState

cmd = typer.Typer()


@cmd.callback(invoke_without_command=True)
def callback(ctx: typer.Context) -> None:
    """Manage EVEData platform configuration."""


@cmd.command(name="list")
def list_(ctx: typer.Context) -> None:
    """List configuration settings."""
    state: AdminState = ctx.obj
    state.out.print(state.config.model_dump())
