from typer import Typer

app = Typer(name="evedata-infra")


@app.command(name="status")
def status_cmd():
    """Check infrastructure status."""
