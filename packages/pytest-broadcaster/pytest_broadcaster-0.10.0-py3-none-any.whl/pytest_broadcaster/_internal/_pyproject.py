from __future__ import annotations

import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib as toml
else:
    import tomli as toml


def get_pyproject() -> Path | None:
    parent_path = Path.cwd()
    while True:
        try_path = parent_path / "pyproject.toml"
        if try_path.exists():
            return try_path
        new_parent = parent_path.parent
        if new_parent == parent_path:
            return None
        parent_path = new_parent
        parent_path = new_parent


def get_pyproject_data(path: Path) -> dict[str, Any]:
    return toml.loads(path.read_text())


def get_project_name(pyproject: dict[str, Any]) -> str:
    if "tool" in pyproject and "poetry" in pyproject["tool"]:
        # https://python-poetry.org/docs/pyproject/#name
        return str(pyproject["tool"]["poetry"]["name"])
    # https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#name
    return str(pyproject["project"]["name"])


def get_project_url(pyproject: dict[str, Any]) -> str | None:
    if "tool" in pyproject and "poetry" in pyproject["tool"]:
        # https://python-poetry.org/docs/pyproject/#repository
        if value := pyproject["tool"]["poetry"].get("repository"):
            return str(value)
        return None

    urls = pyproject["project"].get("urls")
    if urls is None:
        return None
    # I did not find any official doc but repository is listed here:
    # https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#urls
    for key, value in urls.items():
        if key.lower() == "repository":
            return str(value)
        if key.lower() == "source":
            return str(value)
    return None


def get_project_version(name: str) -> str | None:
    try:
        return version(name)
    except PackageNotFoundError:
        return None
