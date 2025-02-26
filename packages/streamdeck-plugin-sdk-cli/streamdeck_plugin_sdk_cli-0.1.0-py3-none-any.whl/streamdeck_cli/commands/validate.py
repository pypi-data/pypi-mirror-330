from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from streamdeck_cli.models.manifest import Manifest


validate_cli = typer.Typer()


@validate_cli.command()
def validate(plugin_dirpath: Optional[Path] = typer.Argument(default=None)):  # noqa: UP007, B008
    plugin_dirpath = plugin_dirpath or Path.cwd()

    if not plugin_dirpath.exists():
        msg = "Provided plugin directory does not exist on machine."
        raise FileNotFoundError(msg)

    manifest_filepath = plugin_dirpath / "manifest.json"

    manifest = Manifest.from_json_file(file=manifest_filepath)

    typer.echo(f"Manifest validation completed successfully for plugin '{manifest.name}'.")



if __name__ == "__main__":
    validate_cli()
