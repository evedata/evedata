from typer import Typer

cmd = Typer()


@cmd.command(name="publish")
def publish_cmd() -> None:
    """Publish reference datasets."""
