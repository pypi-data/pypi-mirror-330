from __future__ import annotations

import logging
import os
import zipfile
from pathlib import Path
from typing import TYPE_CHECKING

import pathspec
import typer
from pathspec.patterns.gitwildmatch import GitWildMatchPattern


if TYPE_CHECKING:
    from collections.abc import Generator



logger = logging.getLogger("streamdeck-cli")


def archive_plugin_files(
    plugin_dirpath: Path,
    output_filepath: Path,
    plugin_uuid: str,
    packignore_spec: pathspec.PathSpec,
    debug_port: int | None = None,
) -> None:
    """Archive the plugin files into a a new zip file."""
    with zipfile.ZipFile(output_filepath, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Files should be stuffed in the zip file under a base directory with the name of the plugin UUID found in the manifest.
        entry_prefix = f"{plugin_uuid}.sdPlugin"

        for filepath in walk_filtered_plugin_files(source_dirpath=plugin_dirpath, packignore_spec=packignore_spec):
            # Ensure these paths are relative to the current working directory, to ensure we're pointing to the actual path.
            arcname: str = os.path.join(entry_prefix, str(filepath)).replace("\\", "/")

            # The full path to the file of the current iteration
            full_filepath: Path = plugin_dirpath / filepath

            logger.debug("%s,  %s", full_filepath, arcname)

            zip_file.write(full_filepath, arcname=arcname)


        # Add a file `.debug` containing the debug port number if debug mode is enabled to the zip file
        if debug_port:
            print("YOOO")
            zip_file.writestr(f"{entry_prefix}/.debug", str(debug_port))


def walk_filtered_plugin_files(source_dirpath: Path, packignore_spec: pathspec.PathSpec) -> Generator[Path, None, None]:
    """Walk through the plugin directory and yield files that are not ignored."""
    # Walk through the directory and yield files that are not ignored
    for root, _dirs, files in os.walk(source_dirpath):
        if packignore_spec.match_file(root):
            continue

        for filename in files:
            filepath = Path(root) / filename
            if packignore_spec.match_file(filepath):
                continue

            # Ensure these paths are relative to the current working directory, to ensure we're pointing to the actual path.
            relative_path = filepath.relative_to(source_dirpath)

            yield relative_path


def get_packignore_specification(source_dirpath: Path) -> pathspec.PathSpec:
    """Get the pathspec specification from the .packignore file."""
    try:
        with (source_dirpath / ".packignore").open("r") as f:
            spec = pathspec.PathSpec.from_lines(GitWildMatchPattern, f)  # type: ignore

    except FileNotFoundError as e:
        typer.echo("ERROR: '.packignore' file is missing from plugin directory...")
        raise typer.Exit(9) from e

    return spec
