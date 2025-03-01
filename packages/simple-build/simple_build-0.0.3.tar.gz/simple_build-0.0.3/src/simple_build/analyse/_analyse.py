"""Analyse a project"""

import ast
from dataclasses import dataclass
from pathlib import Path
import typing as t

from packaging.utils import NormalizedName

from ._pep621 import Author, Pep621Data
from ._pyproject import ToolMetadata, parse_pyproject_toml

PreWriteHook: t.TypeAlias = t.Callable[
    [t.Literal["sdist", "wheel"], Path, str | None, "PackageAnalysis"], None
]
"""A pre-write hook, to modify files before writing them to the sdist or wheel.

:param path: The path to the temporary folder containing the files that will be written to the wheel.
    This can be modified in place, including deleting files and adding new ones.
:param module: The name of the module.
:param package: The package analysis.
"""


@dataclass
class PackageAnalysis:
    """Result of analysing a project."""

    root: Path
    """The root of the project."""
    project: Pep621Data
    """The resolved [project] table."""
    tool: ToolMetadata
    """The resolved [tool.xxx] table."""
    modules: dict[str, Path]
    """The modules in the project."""

    @property
    def name(self) -> NormalizedName:
        """The kebab case name of the project."""
        return self.project["name"]

    @property
    def snake_name(self) -> str:
        """The snake case name of the project."""
        return self.project["name"].replace("-", "_")


def analyse_package(root: Path) -> PackageAnalysis:
    """Analyse a package folder."""
    metadata = parse_pyproject_toml(root)
    proj_config = metadata["project"]
    tool_config = metadata["tool"]

    # find module
    module_name = proj_config["name"].replace("-", "_")
    module_path = None
    for mpath in [
        root / module_name,
        root / "src" / module_name,
        root / (module_name + ".py"),
        root / "src" / (module_name + ".py"),
    ]:
        if mpath.exists():
            module_path = mpath
            break

    # find dynamic keys, raise if any unsatisfied
    if "dynamic" in proj_config:
        if module_path and module_path.is_dir():
            mod_info = read_ast_info(module_path / "__init__.py")
        elif module_path:
            mod_info = read_ast_info(module_path)
        else:
            mod_info = {}
        missing = set(proj_config["dynamic"]) - set(mod_info)  # type: ignore[arg-type]
        if missing:
            raise KeyError(f"Dynamic keys {missing} not found: {root}")
        dynamic_key: t.Literal["description", "version", "authors"]
        for dynamic_key, dynamic_value in mod_info.items():  # type: ignore[assignment]
            if dynamic_key in proj_config["dynamic"]:
                proj_config[dynamic_key] = dynamic_value  # type: ignore[typeddict-item]

    return PackageAnalysis(
        root=root,
        project=proj_config,
        tool=tool_config,
        modules={module_name: module_path} if module_path else {},
    )


class AstInfo(t.TypedDict, total=False):
    """The information that can be read from a python file."""

    description: str
    version: str
    authors: list[Author]


def read_ast_info(path: Path) -> AstInfo:
    """Read information from a python file."""
    if not path.exists():
        raise FileNotFoundError(path)
    # read as bytes to enable custom encodings
    with path.open("rb") as f:
        node = ast.parse(f.read())
    data: dict[str, t.Any] = {}  # type: ignore[misc]
    docstring = ast.get_docstring(node)
    if docstring:
        data["description"] = docstring
    for child in node.body:
        # Only use if it's a simple string assignment
        if not (isinstance(child, ast.Assign) and isinstance(child.value, ast.Str)):
            continue
        for variable, key in (
            ("__version__", "version"),
            ("__author__", "name"),
            ("__email__", "email"),
        ):
            if any(
                isinstance(target, ast.Name) and target.id == variable
                for target in child.targets
            ):
                data[key] = child.value.s
    author = {}
    if "name" in data:
        author["name"] = data.pop("name")
    if "email" in data:
        author["email"] = data.pop("email")
    if author:
        data["authors"] = [author]
    return t.cast(AstInfo, data)
