from typer import Typer

cli = Typer(name="evedata-rest-api")


@cli.callback()
def main():
    """Start the EVEData REST API server."""
