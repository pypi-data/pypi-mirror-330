from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from typing import Any

import flask
from typing_extensions import Self
from werkzeug.serving import make_server


class SpyRequest:
    def __init__(self, request: flask.Request) -> None:
        self._method = request.method
        self._path = request.path
        self._query = request.query_string.decode()
        self._bytes = request.get_data()

    def method(self) -> str:
        return self._method

    def path(self) -> str:
        return self._path

    def query_string(self) -> str:
        return self._query

    def json(self) -> dict[str, Any]:
        return json.loads(self._bytes.decode())

    def text(self) -> str:
        return self._bytes.decode()


@dataclass
class Spy:
    received: list[SpyRequest] = field(default_factory=list)

    def count_received(self) -> int:
        return len(self.received)

    def expect_request(self) -> SpyRequest:
        assert self.count_received() == 1, "Expected only one request"
        return self.received[0]


class EmbeddedTestServer:
    def __init__(
        self,
        spy: Spy,
        path: str = "/webhooks/TestWebhook",
        host: str = "127.0.0.1",
        port: int = 8000,
    ) -> None:
        self.spy = spy
        self.thread = self.ServerThread(self.create_app(spy, path), host, port)

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self.thread.shutdown()

    def __enter__(self) -> Self:
        self.start()
        return self

    def __exit__(self, *args: object, **kwargs: object) -> None:
        self.stop()

    def create_app(self, spy: Spy, path: str) -> flask.Flask:
        app = flask.Flask("test-app")

        @app.route(path, methods=["POST"])
        def _() -> dict[str, str]:
            spy.received.append(SpyRequest(request=flask.request))
            return {"status": "OK"}

        return app

    class ServerThread(threading.Thread):
        def __init__(self, app: flask.Flask, host: str, port: int) -> None:
            threading.Thread.__init__(self)
            self.server = make_server(host, port, app)
            self.ctx = app.app_context()
            self.ctx.push()

        def run(self) -> None:
            self.server.serve_forever()

        def shutdown(self) -> None:
            self.server.shutdown()
