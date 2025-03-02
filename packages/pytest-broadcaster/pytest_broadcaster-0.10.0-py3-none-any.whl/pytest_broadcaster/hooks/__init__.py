"""pytest_broadcaster pytest plugin hooks."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from pytest_broadcaster.interfaces import Destination, Reporter


def pytest_broadcaster_add_destination(add: Callable[[Destination], None], /) -> None:
    """Add your own destination.

    This function is called on plugin initialization.

    For instance, in `conftest.py`:

    ```python
    from pytest_broadcaster import HTTPWebhook

    def pytest_broadcaster_add_destination(add):
        add(HTTPWebhook(url="https://example.com"))
        add(HTTPWebhook(url="https://another-example.com"))
    ```

    Then run pytest without any option:

    ```bash
    pytest
    ```
    """


def pytest_broadcaster_set_reporter(_set: Callable[[Reporter], None], /) -> None:
    """Set your own reporter.

    This funciton is called on plugin initialization.

    For instance, in `conftest.py`:

    ```python
    def pytest_broadcaster_set_reporter(set_reporter):
        set_reporter(MyReporter())
    ```

    Then run pytest without any option:

    ```bash
    pytest
    ```
    """
