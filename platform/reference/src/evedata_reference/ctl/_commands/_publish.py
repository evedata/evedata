from typer import Typer

cmd = Typer(name="evedata-reference-publish")


@cmd.command(name="publish")
def publish_cmd() -> None:
    """Publish reference datasets."""
