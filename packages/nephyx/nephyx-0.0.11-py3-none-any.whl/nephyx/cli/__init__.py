import json
from pathlib import Path
import typer
from nephyx.cli.helper import import_app_entrypoint

app = typer.Typer()


@app.command()
def dummy():
    print("DUMMY")

@app.command()
def export_openapi():
    app = import_app_entrypoint()
    openapi = app.openapi()
    with Path("openapi.json").open("w") as f:
        json.dump(openapi, f, indent=2)
