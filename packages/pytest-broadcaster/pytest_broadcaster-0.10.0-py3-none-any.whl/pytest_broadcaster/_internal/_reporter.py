from __future__ import annotations

import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Literal

import pytest

from pytest_broadcaster.__about__ import __version__
from pytest_broadcaster.interfaces import Reporter
from pytest_broadcaster.models.collect_report import CollectReport
from pytest_broadcaster.models.error_message import ErrorMessage
from pytest_broadcaster.models.location import Location
from pytest_broadcaster.models.outcome import Outcome
from pytest_broadcaster.models.session_end import SessionEnd
from pytest_broadcaster.models.session_result import SessionResult
from pytest_broadcaster.models.session_start import SessionStart
from pytest_broadcaster.models.test_case import TestCase
from pytest_broadcaster.models.test_case_call import TestCaseCall
from pytest_broadcaster.models.test_case_end import TestCaseEnd
from pytest_broadcaster.models.test_case_error import TestCaseError
from pytest_broadcaster.models.test_case_report import TestCaseReport
from pytest_broadcaster.models.test_case_setup import TestCaseSetup
from pytest_broadcaster.models.test_case_teardown import TestCaseTeardown
from pytest_broadcaster.models.test_directory import TestDirectory
from pytest_broadcaster.models.test_module import TestModule
from pytest_broadcaster.models.test_suite import TestSuite
from pytest_broadcaster.models.traceback import Entry, Traceback
from pytest_broadcaster.models.warning_message import WarningMessage, When

from . import _fields as api

if TYPE_CHECKING:
    import warnings


class DefaultReporter(Reporter):
    def __init__(
        self,
        session_id: str | None = None,
        clock: Callable[[], datetime.datetime] | None = None,
    ) -> None:
        self._clock = clock or (lambda: datetime.datetime.now(tz=datetime.timezone.utc))
        self._session_id = session_id or api.make_session_id()
        self._python = api.make_python_distribution()
        self._project = api.make_project()
        self._roots: dict[str, str] = {}
        self._pending_report: TestCaseReport | None = None
        self._start_timestamp = api.make_timestamp_from_datetime(self._clock())
        self._result = SessionResult(
            session_id=self._session_id,
            start_timestamp=self._start_timestamp,
            stop_timestamp=self._start_timestamp,  # will be replaced later
            python=self._python,
            pytest_version=pytest.__version__,
            plugin_version=__version__,
            exit_status=0,
            warnings=[],
            errors=[],
            collect_reports=[],
            test_reports=[],
            project=self._project,
        )
        self._done = False

    def _get_path(self, path: str, *, is_error_or_warning: bool = False) -> str:
        for root in self._roots:
            if path.startswith(root):
                return self._roots[root] + "/" + path[len(root) + 1 :]
        pathobj = Path(path)
        if pathobj.is_dir():
            self._roots[path] = pathobj.name
            return pathobj.name
        if pathobj.is_file() and not is_error_or_warning:
            self._roots[path] = pathobj.parent.name
            return f"{pathobj.parent.name}/{pathobj.name}"
        return path

    def make_session_result(self) -> SessionResult | None:
        if not self._done:
            return None
        return self._result

    def make_session_start(self) -> SessionStart:
        return SessionStart(
            session_id=self._session_id,
            timestamp=self._start_timestamp,
            python=self._python,
            pytest_version=pytest.__version__,
            plugin_version=__version__,
            project=self._project,
        )

    def make_session_end(self, exit_status: int) -> SessionEnd:
        stop_timestamp = api.make_timestamp_from_datetime(self._clock())
        self._result.stop_timestamp = stop_timestamp
        self._result.exit_status = exit_status
        self._done = True
        return SessionEnd(
            session_id=self._session_id,
            timestamp=stop_timestamp,
            exit_status=exit_status,
        )

    def make_warning_message(
        self,
        warning_message: warnings.WarningMessage,
        when: Literal["config", "collect", "runtest"],
        nodeid: str,
    ) -> WarningMessage:
        msg = WarningMessage(
            category=warning_message.category.__name__
            if warning_message.category
            else None,
            location=Location(
                filename=self._get_path(
                    warning_message.filename, is_error_or_warning=True
                ),
                lineno=warning_message.lineno,
            ),
            message=api.make_warning_message(warning_message),
            when=When(when),
            node_id=nodeid,
        )
        self._result.warnings.append(msg)
        return msg

    def make_error_message(
        self, report: pytest.CollectReport, call: pytest.CallInfo[Any]
    ) -> ErrorMessage:
        exc_info: pytest.ExceptionInfo[BaseException] | None = call.excinfo
        assert exc_info, "exception info is missing"
        exc_repr = exc_info.getrepr()
        assert exc_repr.reprcrash, "exception crash repr is missing"
        traceback_lines = api.make_traceback_from_reprtraceback(exc_repr.reprtraceback)
        msg = ErrorMessage(
            when=call.when,  # type: ignore[arg-type]
            location=Location(
                filename=self._get_path(
                    exc_repr.reprcrash.path, is_error_or_warning=True
                ),
                lineno=exc_repr.reprcrash.lineno,
            ),
            traceback=Traceback(
                entries=[
                    Entry(
                        lineno=line.lineno,
                        path=line.path,
                        message=line.message,
                    )
                    for line in traceback_lines
                ]
            ),
            exception_type=exc_info.typename,
            exception_value=str(exc_info.value),
        )
        self._result.errors.append(msg)
        return msg

    def make_collect_report(self, report: pytest.CollectReport) -> CollectReport:
        items: list[TestCase | TestDirectory | TestModule | TestSuite] = []
        # Format all test items reported
        for result in report.result:
            if isinstance(result, pytest.Directory):
                items.append(
                    TestDirectory(
                        node_id=result.nodeid,
                        name=result.path.name,
                        path=self._get_path(result.path.as_posix()),
                    )
                )
                continue
            if isinstance(result, pytest.Module):
                items.append(
                    TestModule(
                        node_id=result.nodeid,
                        name=result.name,
                        path=self._get_path(result.path.as_posix()),
                        markers=api.make_markers(result),
                        doc=api.make_doc(result),
                    )
                )
                continue
            if isinstance(result, pytest.Class):
                node_id = api.make_node_id(result)
                assert node_id.module
                items.append(
                    TestSuite(
                        node_id=result.nodeid,
                        name=result.name,
                        module=node_id.module,
                        path=self._get_path(result.path.as_posix()),
                        doc=api.make_doc(result),
                        markers=api.make_markers(result),
                    )
                )
                continue
            if isinstance(result, pytest.Function):
                node_id = api.make_node_id(result)
                item = TestCase(
                    node_id=node_id.value,
                    name=node_id.name,
                    module=node_id.module,
                    suite=node_id.suite(),
                    function=node_id.func,
                    path=self._get_path(result.path.as_posix()),
                    doc=api.make_doc(result),
                    markers=api.make_markers(result),
                    parameters=api.make_parameters(result),
                )
                items.append(item)
        # Generate a collect report event.
        collect_report = CollectReport(
            session_id=self._session_id,
            timestamp=api.make_timestamp_from_datetime(self._clock()),
            node_id=report.nodeid or "",
            items=items,
        )
        self._result.collect_reports.append(collect_report)
        return collect_report

    def make_test_case_step(
        self, report: pytest.TestReport
    ) -> TestCaseCall | TestCaseSetup | TestCaseTeardown:
        # Always validate the outcome
        outcome = Outcome(report.outcome)
        # Let's process the error if any
        error: TestCaseError | None = None
        if report.failed:
            error = TestCaseError(
                message=report.longreprtext,
                traceback=Traceback(
                    entries=[
                        Entry(path=line.path, lineno=line.lineno, message=line.message)
                        for line in api.make_traceback(report)
                    ]
                ),
            )
        # Let's process the report based on the step
        step: TestCaseSetup | TestCaseCall | TestCaseTeardown
        if report.when == "setup":
            step = TestCaseSetup(
                session_id=self._session_id,
                node_id=report.nodeid,
                start_timestamp=api.make_timestamp(report.start),
                stop_timestamp=api.make_timestamp(report.stop),
                duration=report.duration,
                outcome=outcome,
                error=error,
            )
            self._pending_report = TestCaseReport(
                node_id=report.nodeid,
                outcome=outcome,
                duration=step.duration,
                setup=step,
                teardown=...,  # type: ignore[arg-type]
                finished=...,  # type: ignore[arg-type]
            )
        elif report.when == "call":
            if outcome == Outcome.skipped and hasattr(report, "wasxfail"):
                outcome = Outcome.xfailed
            step = TestCaseCall(
                session_id=self._session_id,
                node_id=report.nodeid,
                start_timestamp=api.make_timestamp(report.start),
                stop_timestamp=api.make_timestamp(report.stop),
                duration=report.duration,
                outcome=outcome,
                error=error,
            )
            assert self._pending_report, (
                "pending report is missing, this is a bug in pytest-broadcaster plugin"
            )
            self._pending_report.call = step

        elif report.when == "teardown":
            step = TestCaseTeardown(
                session_id=self._session_id,
                node_id=report.nodeid,
                outcome=outcome,
                duration=report.duration,
                error=error,
                start_timestamp=api.make_timestamp(report.start),
                stop_timestamp=api.make_timestamp(report.stop),
            )
            assert self._pending_report, (
                "pending report is missing, this is a bug in pytest-broadcaster plugin"
            )
            self._pending_report.teardown = step
        else:
            msg = f"Unknown step {report.when}"
            raise ValueError(msg)
        return step

    def make_test_case_end(self, node_id: str) -> TestCaseEnd:
        # Let's pop the pending report (we always have one)
        pending_report = self._pending_report
        self._pending_report = None
        assert pending_report, (
            "pending report is missing, this is a bug in pytest-broadcaster plugin"
        )
        assert pending_report.node_id == node_id, (
            "node_id mismatch, this is a bug in pytest-broadcaster plugin"
        )
        # Get all reports
        reports = [
            report
            for report in (
                pending_report.setup,
                pending_report.call,
                pending_report.teardown,
            )
            if report is not None
        ]
        # Detect if test was failed
        if any(report.outcome == Outcome.failed for report in reports):
            outcome = Outcome.failed
        elif any(report.outcome == Outcome.xfailed for report in reports):
            outcome = Outcome.xfailed
        # Detect if test was skipped
        elif any(report.outcome == Outcome.skipped for report in reports):
            outcome = Outcome.skipped
        # Else consider test passed
        else:
            outcome = Outcome.passed
        duration = sum(report.duration for report in reports)
        # Create the finished event
        finished = TestCaseEnd(
            session_id=self._session_id,
            node_id=node_id,
            start_timestamp=pending_report.setup.start_timestamp,
            stop_timestamp=pending_report.teardown.stop_timestamp,
            total_duration=duration,
            outcome=outcome,
        )
        # Create the report
        report = TestCaseReport(
            node_id=node_id,
            outcome=finished.outcome,
            duration=finished.total_duration,
            finished=finished,
            setup=pending_report.setup,
            call=pending_report.call,
            teardown=pending_report.teardown,
        )
        self._result.test_reports.append(report)
        return finished


if TYPE_CHECKING:
    # Make sure that the class implements the interface
    DefaultReporter("fake-id", datetime.datetime.now)
