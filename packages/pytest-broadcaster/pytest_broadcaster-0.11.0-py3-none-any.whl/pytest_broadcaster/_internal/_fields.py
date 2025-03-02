from __future__ import annotations

import datetime
import importlib.metadata
import platform
import sys
from typing import TYPE_CHECKING
from uuid import uuid4

from pytest_broadcaster.models.project import Project
from pytest_broadcaster.models.python_distribution import (
    Package,
    Platform,
    PythonDistribution,
    Releaselevel,
    Version,
)

from ._pyproject import (
    get_project_name,
    get_project_url,
    get_project_version,
    get_pyproject,
    get_pyproject_data,
)
from ._utils import (
    NodeID,
    TracebackLine,
    filter_traceback,
    format_mark,
    get_test_args,
    get_test_doc,
    get_test_markers,
    make_traceback_line,
    parse_node_id,
)

if TYPE_CHECKING:
    from warnings import WarningMessage

    import pytest
    from _pytest._code.code import ReprTraceback


def make_session_id() -> str:
    return str(uuid4())


def make_node_id(
    item: pytest.Item | pytest.Directory | pytest.Module | pytest.Class,
) -> NodeID:
    mod, cls, func, params = parse_node_id(item.nodeid)
    name = f"{func}[{params}]" if params else func
    filename = mod.split("/")[-1] if mod else None
    module = filename.replace(".py", "") if filename else None
    classes = cls.split("::") if cls else None
    return NodeID(
        filename=filename,
        module=module,
        classes=classes,
        func=func,
        params=params or None,
        name=name,
        value=item.nodeid,
    )


def make_doc(item: pytest.Item | pytest.Module | pytest.Class) -> str:
    return get_test_doc(item).strip()


def make_markers(
    item: pytest.Item | pytest.Directory | pytest.Module | pytest.Class,
) -> list[str]:
    return list(
        {
            format_mark(mark)
            for mark in sorted(get_test_markers(item), key=lambda mark: mark.name)
        }
    )


def make_parameters(item: pytest.Item) -> dict[str, str]:
    return {k: type(v).__name__ for k, v in sorted(get_test_args(item).items())}


def make_python_distribution() -> PythonDistribution:
    packages = [
        Package(name=x.metadata.get("Name"), version=x.version)  # pyright: ignore[reportAttributeAccessIssue]
        for x in importlib.metadata.distributions()
    ]
    raw_platform_os = platform.system()
    if raw_platform_os == "Linux":
        platform_os = Platform.linux
    elif raw_platform_os == "Darwin":
        platform_os = Platform.darwin
    elif raw_platform_os == "Windows":
        platform_os = Platform.windows
    elif raw_platform_os == "Java":
        platform_os = Platform.java
    else:
        platform_os = Platform.unknown
    processor_architecture = platform.processor()
    raw_level = sys.version_info.releaselevel
    if raw_level == "final":
        level = Releaselevel.final
    elif raw_level == "beta":
        level = Releaselevel.beta
    elif raw_level == "alpha":
        level = Releaselevel.alpha
    else:
        level = Releaselevel.candidate
    return PythonDistribution(
        version=Version(
            major=sys.version_info.major,
            minor=sys.version_info.minor,
            micro=sys.version_info.micro,
            releaselevel=level,
        ),
        packages=packages,
        platform=platform_os,
        processor=processor_architecture,
    )


def make_project() -> Project | None:
    pyproject_path = get_pyproject()
    if pyproject_path is None:
        return None
    pyproject_data = get_pyproject_data(pyproject_path)
    project_name = get_project_name(pyproject_data)
    project_url = get_project_url(pyproject_data)
    project_version = get_project_version(project_name)
    return Project(project_name, project_version, project_url)


def make_warning_message(warning: WarningMessage) -> str:
    if isinstance(warning.message, str):
        return warning.message
    return str(warning.message)


def make_timestamp(epoch: float) -> str:
    return datetime.datetime.fromtimestamp(epoch, tz=datetime.timezone.utc).isoformat()


def make_timestamp_from_datetime(dt: datetime.datetime) -> str:
    return dt.astimezone(datetime.timezone.utc).isoformat()


def make_traceback(report: pytest.TestReport) -> list[TracebackLine]:
    return make_traceback_from_reprtraceback(report.longrepr.reprtraceback)  # type: ignore[union-attr]


def make_traceback_from_reprtraceback(
    reprtraceback: ReprTraceback,
) -> list[TracebackLine]:
    return [
        make_traceback_line(line.reprfileloc)  # type: ignore[union-attr, arg-type]
        for line in reprtraceback.reprentries
        if filter_traceback(line.reprfileloc.path)  # type: ignore[union-attr]
    ]
