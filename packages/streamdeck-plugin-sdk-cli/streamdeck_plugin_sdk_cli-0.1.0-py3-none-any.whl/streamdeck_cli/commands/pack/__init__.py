"""Pack/build a Stream Deck plugin into a .streamDeckPlugin file."""
import logging
from pathlib import Path
from typing import Optional

import pathspec
import typer

from streamdeck_cli.commands.pack.autoversion import get_versioned_output_dirpath
from streamdeck_cli.commands.pack.zip import archive_plugin_files, get_packignore_specification
from streamdeck_cli.models.manifest import Manifest


logger = logging.getLogger("streamdeck-cli")
logger.setLevel(logging.DEBUG)


pack_cli = typer.Typer()


@pack_cli.command()
def pack(
    plugin_dirpath: Path = typer.Argument(  # noqa: B008
        ...,
        default_factory=Path.cwd,
        help="Path to the plugin directory",
    ),
    output_dirpath: Path = typer.Option(  # noqa: B008
        ...,
        "--output",
        "-o",
        default_factory=lambda: Path.cwd() / "releases",
        help="Output directory",
    ),
    version: Optional[str] = None,  # noqa: UP007
    debug_port: Optional[int] = typer.Option(
        None,
        "--debug",
        "-d",
        help="Enable debug mode in the packed plugin to listen for debug messages on the specified port",
    ),
) -> None:
    """Pack/build a Stream Deck plugin into a .streamDeckPlugin file."""
    # Validate the manifest by initiating its model.
    manifest = Manifest.from_json_file(plugin_dirpath / "manifest.json")

    # Determine the versioned output directory name
    version_dirname = version or manifest.version

    # Get the versioned output directory path
    versioned_output_dirpath = get_versioned_output_dirpath(output_dirpath, version_dirname)

    # Define the full output file path for the plugin.
    # The output file at this path will be a .streamDeckPlugin file, which will open the plugin in the Stream Deck app.
    # The output file at this path is a zip file containing the files of the plugin, which the Stream Deck software unzips to a specific app directory.
    output_filepath = versioned_output_dirpath / f"{manifest.uuid}.streamDeckPlugin"
    logger.info("Output plugin file will be created at: %s", output_filepath)

    # Create the package directory
    versioned_output_dirpath.mkdir(parents=True, exist_ok=True)

    # Get the .packignore specification to filter out files that should not be included in the plugin package
    pathignore_spec: pathspec.PathSpec = get_packignore_specification(plugin_dirpath)

    # Create the zip file and add the plugin files
    archive_plugin_files(
        plugin_dirpath,
        output_filepath,
        plugin_uuid=manifest.uuid,
        packignore_spec=pathignore_spec,
        debug_port=debug_port,
    )


if __name__ == "__main__":
    pack_cli()
