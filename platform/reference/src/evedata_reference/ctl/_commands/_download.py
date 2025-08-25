from typer import Typer

cmd = Typer(name="evedata-reference-download")


@cmd.command(name="download")
def download_cmd() -> None:
    """Download raw reference sources."""
