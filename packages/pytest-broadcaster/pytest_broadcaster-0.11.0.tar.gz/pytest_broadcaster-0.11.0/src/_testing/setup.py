from __future__ import annotations

import json
from copy import deepcopy
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from pathlib import Path


class CommonTestSetup:
    @pytest.fixture(autouse=True)
    def setup(
        self, pytester: pytest.Pytester, tmp_path: Path, pytestconfig: pytest.Config
    ) -> None:
        self.tmp_path = tmp_path
        self.test_dir = pytester
        self.pytestconfig = pytestconfig
        self.json_file = self.tmp_path.joinpath("collect.json")
        self.json_lines_file = self.tmp_path.joinpath("collect.jsonl")

    def read_json_file(self) -> dict[str, Any]:
        return json.loads(self.json_file.read_text())

    def read_json_lines_file(self) -> list[dict[str, Any]]:
        return [
            json.loads(line.strip())
            for line in self.json_lines_file.read_text().splitlines()
            if line.strip()
        ]

    def make_testfile(self, filename: str, content: str) -> Path:
        if filename.endswith(".py"):
            filename = filename[:-3]
        else:
            msg = "Filename must end with '.py'"
            raise ValueError(msg)
        kwargs = {filename: content}
        return self.test_dir.makepyfile(**kwargs)  # pyright: ignore[reportUnknownMemberType]

    def sanitize(self, data: object) -> object:
        return self._sanitize(deepcopy(data))

    def _sanitize(
        self,
        data: object,
    ) -> object:
        if isinstance(data, dict):
            for key, value in data.items():  # pyright: ignore[reportUnknownVariableType]
                if key == "traceback":
                    data[key] = {
                        **data[key],
                        "entries": [
                            line
                            for line in value["entries"]  # pyright: ignore[reportUnknownVariableType]
                            if (
                                "importlib" not in line["path"]
                                and "pytest_asyncio" not in line["path"]
                            )
                        ],
                    }
                elif key in (
                    "duration",
                    "total_duration",
                    "start_timestamp",
                    "stop_timestamp",
                    "timestamp",
                    "platform",
                    "processor",
                    "session_id",
                ):
                    data[key] = "omitted"
                elif key == "packages":
                    data[key] = {}
                elif isinstance(value, (dict, list)):
                    data[key] = self._sanitize(value)
        elif isinstance(data, list):
            data = [self._sanitize(item) for item in data]
        else:
            return data
        return data  # pyright: ignore[reportUnknownVariableType]
