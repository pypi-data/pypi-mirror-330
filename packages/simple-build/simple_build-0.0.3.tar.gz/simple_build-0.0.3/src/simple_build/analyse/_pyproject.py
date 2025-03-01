"""Read the pyproject.toml file, parse and validate it."""

from pathlib import Path, PurePosixPath
from pydoc import importfile
import re
import tomllib
import typing as t

from ._pep621 import Pep621Data, ProjectValidationError
from ._pep621 import parse as parse_project

if t.TYPE_CHECKING:
    from ._analyse import PreWriteHook


def read_pyproject_toml(path: Path) -> dict[str, t.Any]:  # type: ignore[misc]
    """Read the pyproject.toml file.

    :returns: The contents of the pyproject.toml file.
    """
    return tomllib.loads(path.read_text("utf-8"))


class PyMetadata(t.TypedDict):
    """The parsed pyproject.toml file."""

    project: Pep621Data
    tool: "ToolMetadata"


def parse_pyproject_toml(root: Path) -> PyMetadata:
    """Read the pyproject.toml file, parse and validate it."""
    pyproject_file = root.joinpath("pyproject.toml")
    if not pyproject_file.exists():
        raise FileNotFoundError(pyproject_file)
    metadata = read_pyproject_toml(pyproject_file)
    # parse and validate the project configuration
    project_result = parse_project(metadata, root)
    # parse and validate the tool configuration
    tool_result = resolve_tool_section(metadata, root, "build")

    errors = project_result.errors + tool_result.errors
    if errors:
        raise RuntimeError(
            "Error(s) parsing {}:\n{}".format(
                pyproject_file, "\n".join(f"- {e}" for e in errors)
            )
        )

    return {"project": project_result.data, "tool": tool_result.data}


class SdistMetadata(t.TypedDict, total=False):
    """The sdist build configuration."""

    use_git: bool
    """Whether to use git to determine tracked files (default True)."""
    include: list[str]
    """The list of additional files to include in the sdist."""
    exclude: list[str]
    """The list of files to exclude from the sdist."""


class ToolMetadata(t.TypedDict, total=False):
    """The parsed tool configuration."""

    sdist: "SdistMetadata"
    """The sdist build configuration."""
    pre_write_hooks: list["PreWriteHook"]
    """The list of pre-write hooks."""


class ParseToolResult(t.NamedTuple):
    """The resolved [tool.monorepo] table configuration."""

    data: ToolMetadata
    errors: list[ProjectValidationError]


def resolve_tool_section(  # type: ignore[misc]
    metadata: dict[str, t.Any], root: Path, tool_section: str
) -> ParseToolResult:
    """Parse the tool configuration."""
    result = ParseToolResult({}, [])

    tool = metadata.get("tool", {})
    if not isinstance(tool, dict):
        result.errors.append(ProjectValidationError("tool", "type", "must be a table"))
        return result

    config = tool.get(tool_section, {})
    if not isinstance(config, dict):
        result.errors.append(
            ProjectValidationError(f"tool.{tool_section}", "type", "must be a table")
        )
        return result

    if "pre_write_hooks" in config:
        if not isinstance(config["pre_write_hooks"], list):
            result.errors.append(
                ProjectValidationError(
                    f"tool.{tool_section}.pre_write_hooks", "type", "must be a list"
                )
            )
        else:
            result.data["pre_write_hooks"] = []
            for hook in config["pre_write_hooks"]:
                if not isinstance(hook, str):
                    result.errors.append(
                        ProjectValidationError(
                            f"tool.{tool_section}.pre_write_hooks",
                            "type",
                            "must be a list of strings",
                        )
                    )
                else:
                    # TODO improve this
                    result.data["pre_write_hooks"].append(
                        importfile(hook).pre_write_hook
                    )

    if "sdist" in config:
        if not isinstance(config["sdist"], dict):
            result.errors.append(
                ProjectValidationError(
                    f"tool.{tool_section}.sdist", "type", "must be a table"
                )
            )
        else:
            sresult = _resolve_tool_sdist_section(config["sdist"], root, tool_section)
            result.data["sdist"] = sresult[0]
            result.errors.extend(sresult[1])

    return result


def _resolve_tool_sdist_section(  # type: ignore[misc] # noqa: PLR0912
    config: dict[str, t.Any], root: Path, tool_section: str
) -> tuple[SdistMetadata, list[ProjectValidationError]]:
    """Parse the sdist configuration."""
    result: SdistMetadata = {}
    errors: list[ProjectValidationError] = []

    if "use_git" in config:
        if not isinstance(config["use_git"], bool):
            errors.append(
                ProjectValidationError(
                    f"tool.{tool_section}.use_git", "type", "must be a boolean"
                )
            )
        else:
            result["use_git"] = config["use_git"]

    if "include" in config:
        if not isinstance(config["include"], list):
            errors.append(
                ProjectValidationError(
                    f"tool.{tool_section}.include", "type", "must be a list"
                )
            )
        else:
            result["include"] = []
            for idx, path in enumerate(config["include"]):
                rel_path = _validate_glob(
                    path, f"tool.{tool_section}.include.{idx}", errors
                )
                if rel_path is not None:
                    result["include"].append(rel_path)

    if "exclude" in config:
        if not isinstance(config["exclude"], list):
            errors.append(
                ProjectValidationError(
                    f"tool.{tool_section}.exclude", "type", "must be a list"
                )
            )
        else:
            result["exclude"] = []
            for idx, path in enumerate(config["exclude"]):
                rel_path = _validate_glob(
                    path, f"tool.{tool_section}.exclude.{idx}", errors
                )
                if rel_path is not None:
                    result["exclude"].append(rel_path)

    return result, errors


_BAD_GLOB_CHARS_RGX = r"[\x00-\x1f\x7f]"
"""Windows filenames can't contain these; https://stackoverflow.com/a/31976060/434217"""


def _validate_glob(
    value: str, key: str, errors: list[ProjectValidationError]
) -> str | None:
    """Validate a glob pattern.

    :param value: A glob pattern.
    :param key: The key of the glob in the project table.
    :param errors: The list of validation errors. to append to.
    """
    if not isinstance(value, str):
        errors.append(ProjectValidationError(key, "type", "must be a string"))
        return None
    if re.search(_BAD_GLOB_CHARS_RGX, value):
        errors.append(
            ProjectValidationError(
                key, "value", "glob must not contain control characters"
            )
        )
        return None
    if value.endswith("/"):
        value += "**/*"
    try:
        rel_glob = PurePosixPath(value)
    except Exception as exc:
        errors.append(ProjectValidationError(key, "value", f"invalid glob: {exc}"))
        return None
    if rel_glob.is_absolute():
        errors.append(ProjectValidationError(key, "value", "glob must be relative"))
        return None
    if ".." in rel_glob.parts:
        errors.append(
            ProjectValidationError(key, "value", "glob must not contain '..'")
        )
        return None
    return rel_glob.as_posix()
