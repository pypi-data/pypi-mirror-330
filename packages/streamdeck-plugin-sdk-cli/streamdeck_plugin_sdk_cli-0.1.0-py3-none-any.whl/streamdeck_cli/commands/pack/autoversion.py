import re
from pathlib import Path


def get_subversion(full_version: Path) -> int:
    """Get the subversion number from the full version name.

    If there isn't a subversion number (e.g. "1.0.0"), then return 0.
    """
    subversion_match: list[int] = re.findall(r"-(\d+)$", full_version.name)

    if not subversion_match:
        return 0

    return int(subversion_match[-1])


def get_versioned_output_dirpath(output_dirpath: Path, plugin_version: str) -> Path:
    """Get the versioned output directory path for the plugin to be created.

    This function will check for previous releases with the same version and increment the subversion if necessary.
    """
    # Check for previous releases with the same version and increment the version if necessary
    previous_releases_with_same_version: list[Path] = sorted(output_dirpath.glob(f"{plugin_version}*"), key=get_subversion)

    if previous_releases_with_same_version:
        # If there is only one release with the same version, just append "-1" to the version
        if len(previous_releases_with_same_version) == 1:
            plugin_version = f"{plugin_version}-1"

        # If there are multiple releases with the same version, then sub-versions have already been appended, so we need to increment the last sub-version
        else:
            # Get the last release directory name
            previous_release_dirpath = previous_releases_with_same_version[-1]
            # Use regex to extract sub-versions from the previous release directory name
            previous_release_dirname_subversion = get_subversion(previous_release_dirpath)

            # Get the previous release directory name before the sub-version
            previous_release_dirname_no_subversion = previous_release_dirpath.name.split("-")[0]
            # Increment the sub-version and create the new versioned directory name for the plugin
            plugin_version = f"{previous_release_dirname_no_subversion}-{int(previous_release_dirname_subversion)+1}"

    # Return the output directory path for the new version of the plugin to be created
    return output_dirpath / plugin_version