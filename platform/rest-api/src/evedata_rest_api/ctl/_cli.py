from typer import Typer

cli = Typer(name="evedata-rest-api")


@cli.callback()
def main():
    """Start the REST API."""
