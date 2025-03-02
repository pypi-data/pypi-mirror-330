from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest

from _testing.setup import CommonTestSetup
from pytest_broadcaster import __version__

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.suites
@pytest.mark.basic
class TestBasicSuite(CommonTestSetup):
    """Test several tests cases within a single test suite within a single test file."""

    def make_test_directory(self) -> Path:
        return self.make_testfile(
            "test_basic_suite.py",
            """
            '''This is a module docstring.'''
            class TestOk:
                '''This is a suite docstring.'''
                def test_1():
                    '''This is a first docstring.'''
                    pass
                def test_2():
                    '''This is a second docstring.'''
                    pass
            """,
        ).parent

    def test_json(self):
        """Test JSON report for single test suite within a single test file."""
        directory = self.make_test_directory()
        result = self.test_dir.runpytest(
            "--collect-only", "--collect-report", self.json_file.as_posix()
        )
        assert result.ret == 0
        assert self.json_file.exists()
        assert self.sanitize(self.read_json_file()) == {
            "session_id": "omitted",
            "start_timestamp": "omitted",
            "stop_timestamp": "omitted",
            "project": None,
            "python": {
                "version": {
                    "major": sys.version_info.major,
                    "minor": sys.version_info.minor,
                    "micro": sys.version_info.micro,
                    "releaselevel": sys.version_info.releaselevel,
                },
                "platform": "omitted",
                "processor": "omitted",
                "packages": {},
            },
            "pytest_version": pytest.__version__,
            "plugin_version": __version__,
            "exit_status": 0,
            "errors": [],
            "warnings": [],
            "test_reports": [],
            "collect_reports": [
                {
                    "event": "collect_report",
                    "session_id": "omitted",
                    "node_id": "",
                    "timestamp": "omitted",
                    "items": [
                        {
                            "node_id": ".",
                            "node_type": "directory",
                            "name": directory.name,
                            "path": directory.name,
                        }
                    ],
                },
                {
                    "event": "collect_report",
                    "session_id": "omitted",
                    "node_id": "test_basic_suite.py::TestOk",
                    "timestamp": "omitted",
                    "items": [
                        {
                            "node_id": "test_basic_suite.py::TestOk::test_1",
                            "node_type": "case",
                            "name": "test_1",
                            "doc": "This is a first docstring.",
                            "markers": [],
                            "parameters": {},
                            "path": directory.joinpath("test_basic_suite.py")
                            .relative_to(directory.parent)
                            .as_posix(),
                            "module": "test_basic_suite",
                            "suite": "TestOk",
                            "function": "test_1",
                        },
                        {
                            "node_id": "test_basic_suite.py::TestOk::test_2",
                            "node_type": "case",
                            "name": "test_2",
                            "doc": "This is a second docstring.",
                            "markers": [],
                            "parameters": {},
                            "path": directory.joinpath("test_basic_suite.py")
                            .relative_to(directory.parent)
                            .as_posix(),
                            "module": "test_basic_suite",
                            "suite": "TestOk",
                            "function": "test_2",
                        },
                    ],
                },
                {
                    "event": "collect_report",
                    "session_id": "omitted",
                    "node_id": "test_basic_suite.py",
                    "timestamp": "omitted",
                    "items": [
                        {
                            "node_id": "test_basic_suite.py::TestOk",
                            "node_type": "suite",
                            "name": "TestOk",
                            "path": directory.joinpath("test_basic_suite.py")
                            .relative_to(directory.parent)
                            .as_posix(),
                            "module": "test_basic_suite",
                            "doc": "This is a suite docstring.",
                            "markers": [],
                        }
                    ],
                },
                {
                    "event": "collect_report",
                    "session_id": "omitted",
                    "node_id": ".",
                    "timestamp": "omitted",
                    "items": [
                        {
                            "node_id": "test_basic_suite.py",
                            "node_type": "module",
                            "name": "test_basic_suite.py",
                            "path": directory.joinpath("test_basic_suite.py")
                            .relative_to(directory.parent)
                            .as_posix(),
                            "doc": "This is a module docstring.",
                            "markers": [],
                        }
                    ],
                },
            ],
        }

    def test_jsonl(self):
        """Test JSON Lines report for single test suite within a single test file."""
        directory = self.make_test_directory()
        result = self.test_dir.runpytest(
            "--collect-only", "--collect-log", self.json_lines_file.as_posix()
        )
        assert result.ret == 0
        assert self.json_lines_file.exists()
        assert self.sanitize(self.read_json_lines_file()) == [
            {
                "session_id": "omitted",
                "timestamp": "omitted",
                "project": None,
                "python": {
                    "version": {
                        "major": sys.version_info.major,
                        "minor": sys.version_info.minor,
                        "micro": sys.version_info.micro,
                        "releaselevel": sys.version_info.releaselevel,
                    },
                    "platform": "omitted",
                    "processor": "omitted",
                    "packages": {},
                },
                "pytest_version": pytest.__version__,
                "plugin_version": __version__,
                "event": "session_start",
            },
            {
                "event": "collect_report",
                "session_id": "omitted",
                "node_id": "",
                "timestamp": "omitted",
                "items": [
                    {
                        "node_id": ".",
                        "node_type": "directory",
                        "name": directory.name,
                        "path": directory.name,
                    }
                ],
            },
            {
                "event": "collect_report",
                "session_id": "omitted",
                "node_id": "test_basic_suite.py::TestOk",
                "timestamp": "omitted",
                "items": [
                    {
                        "node_id": "test_basic_suite.py::TestOk::test_1",
                        "node_type": "case",
                        "name": "test_1",
                        "doc": "This is a first docstring.",
                        "markers": [],
                        "parameters": {},
                        "path": directory.joinpath("test_basic_suite.py")
                        .relative_to(directory.parent)
                        .as_posix(),
                        "module": "test_basic_suite",
                        "suite": "TestOk",
                        "function": "test_1",
                    },
                    {
                        "node_id": "test_basic_suite.py::TestOk::test_2",
                        "node_type": "case",
                        "name": "test_2",
                        "doc": "This is a second docstring.",
                        "markers": [],
                        "parameters": {},
                        "path": directory.joinpath("test_basic_suite.py")
                        .relative_to(directory.parent)
                        .as_posix(),
                        "module": "test_basic_suite",
                        "suite": "TestOk",
                        "function": "test_2",
                    },
                ],
            },
            {
                "event": "collect_report",
                "session_id": "omitted",
                "node_id": "test_basic_suite.py",
                "timestamp": "omitted",
                "items": [
                    {
                        "node_id": "test_basic_suite.py::TestOk",
                        "node_type": "suite",
                        "name": "TestOk",
                        "path": directory.joinpath("test_basic_suite.py")
                        .relative_to(directory.parent)
                        .as_posix(),
                        "doc": "This is a suite docstring.",
                        "module": "test_basic_suite",
                        "markers": [],
                    }
                ],
            },
            {
                "event": "collect_report",
                "session_id": "omitted",
                "node_id": ".",
                "timestamp": "omitted",
                "items": [
                    {
                        "node_id": "test_basic_suite.py",
                        "node_type": "module",
                        "name": "test_basic_suite.py",
                        "path": directory.joinpath("test_basic_suite.py")
                        .relative_to(directory.parent)
                        .as_posix(),
                        "doc": "This is a module docstring.",
                        "markers": [],
                    }
                ],
            },
            {
                "exit_status": 0,
                "event": "session_end",
                "session_id": "omitted",
                "timestamp": "omitted",
            },
        ]
