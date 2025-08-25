from typer import Typer

cmd = Typer()


@cmd.command(name="download")
def download_cmd() -> None:
    """Download raw reference sources."""
