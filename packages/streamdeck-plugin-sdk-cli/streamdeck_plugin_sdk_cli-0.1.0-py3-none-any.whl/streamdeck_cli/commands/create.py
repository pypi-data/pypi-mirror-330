from __future__ import annotations

import copier
import typer
from typing_extensions import TypeAlias  # noqa: UP035


create_cli = typer.Typer()


DirOrVcsPathStr: TypeAlias = str



@create_cli.command()
def create(
    src_path: DirOrVcsPathStr = "https://github.com/strohganoff/python-streamdeck-plugin-template.git",
) -> None:
    """Create a new Stream Deck plugin project from the template."""
    copier.run_copy(
        src_path=src_path,
        unsafe=True,
    )






if __name__ == "__main__":
    create_cli()
