from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from pprint import pprint
from typing import Annotated, ClassVar, Final, Literal, Optional

# import pyjson5
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    Field,
    PrivateAttr,
    ValidationInfo,
    computed_field,
    model_validator,
)
from typing_extensions import Self  # noqa: UP035


def check_path_exists(value: Path, info: ValidationInfo) -> Path:
    context: dict[Literal["manifest_filepath"], Path] = info.context
    plugin_dir: Path = context["manifest_filepath"].parent
    expected_filepath = plugin_dir / value

    assert expected_filepath.exists(), f"Value of '{info.field_name}' field not found."

    return value


def check_image_asset(value: Path, info: ValidationInfo) -> Path:
    # The specified path should not include the file-type suffix.
    assert value.suffix == ""

    context: dict[Literal["manifest_filepath"], Path] = info.context
    plugin_dir: Path = context["manifest_filepath"].parent
    expected_asset_file_basename = plugin_dir / value

    # The image asset should be either svg, png, or gif file-type.
    assert (
        expected_asset_file_basename.with_suffix(".svg").exists() or
        expected_asset_file_basename.with_suffix(".png").exists() or
        expected_asset_file_basename.with_suffix(".gif").exists()
    ), f"Provided image file value for the '{info.field_name}' field does not exist."

    return value


def check_version_format(value: str, _info: ValidationInfo) -> str:
    version_pattern: re.Pattern[str] = re.compile(r"^(0|[1-9]\d*)(\.(0|[1-9]\d*)){2,3}$")

    if not version_pattern.match(value):
        msg = "Version fields should in the format `{major}.{minor}.{patch}` or `{major}.{minor}.{patch}.{build}`."
        raise ValueError(msg)

    return value


class Manifest(BaseModel, extra="allow"):
    _filepath: Path

    uuid: Annotated[str, Field(..., alias="UUID")]
    name: Annotated[str, Field(..., alias="Name")]
    version: Annotated[str, Field(..., alias="Version"), BeforeValidator(check_version_format)]
    author: Annotated[str, Field(..., alias="Author")]
    description: Annotated[str, Field(..., alias="Description")]
    category: Annotated[
        Optional[str],
        Field(..., alias="Category")
    ] = None
    category_icon: Annotated[
        Optional[Path],
        Field(..., alias="CategoryIcon"),
        AfterValidator(check_image_asset),
    ] = None
    actions: Annotated[list[Action], Field(..., alias="Actions")]
    icon: Annotated[
        Path,
        Field(..., alias="Icon"),
        AfterValidator(check_image_asset),
    ]
    code_path: Annotated[
        Path,
        Field(..., alias="CodePath"),
        AfterValidator(check_path_exists)
    ]
    code_path_mac: Annotated[
        Optional[Path],  # noqa: UP007
        Field(..., alias="CodePathMac"),
        AfterValidator(check_path_exists)
    ] = None
    code_path_win: Annotated[
        Optional[Path],  # noqa: UP007
        Field(..., alias="CodePathWin"),
        AfterValidator(check_path_exists)
    ] = None

    @classmethod
    def from_json_file(cls, file: Path):
        """Alternative constructor method.

        This constructor can load data from a json file that contains comments.
        """
        try:
            with file.open("r") as f:
                # contents = f.read()
                contents = json.load(f)

        except FileNotFoundError:
            print("The specified 'manifest.json' filepath does not exist on machine.")
            raise

        else:
            instance = cls.model_validate(contents, context={"manifest_filepath": file})
            instance._filepath = file

            return instance

    @model_validator(mode="after")
    def check_uuids(self) -> Self:
        # The plugin's UUID must be 3 period-delimited parts.
        plugin_uuid_pattern = re.compile(r"^[a-z0-9-]+(\.[a-z0-9-]+){2}$")
        plugin_uuid_match = plugin_uuid_pattern.match(self.uuid)
        if plugin_uuid_match is None:
            msg = "Plugin UUID must have exactly 3 period-delimited segments."
            raise ValueError(msg)

        # Actions of the plugin must have UUID's that are 4 period-delimited parts.
        # plugin_uuid = re.escape(plugin_uuid_match.group())
        plugin_uuid = plugin_uuid_match.group()
        action_pattern = re.compile(rf"^{re.escape(plugin_uuid)}\.[a-z0-9-_]+$")
        for action in self.actions:
            if not action_pattern.match(action.uuid):
                msg = (
                    f"UUID of action '{action.name}' must start with the plugin UUID "
                    f"and have exactly 4 period-delimited segments. plugin_uuid: {plugin_uuid} — action_uuid: {action.uuid}"
                )
                raise ValueError(msg)

        return self



class Action(BaseModel, extra="allow"):
    uuid: Annotated[str, Field(..., alias="UUID")]
    name: Annotated[str, Field(..., alias="Name")]
    icon: Annotated[
        Path,
        Field(..., alias="Icon"),
        AfterValidator(check_image_asset)
    ]
    # This one is optional as long as the plugin-level 'PropertyInspectorPath' field is defined.
    property_inspector_path: Annotated[
        Optional[Path],  # noqa: UP007
        Field(..., alias="PropertyInspectorPath"),
        AfterValidator(check_path_exists)
    ] = None
