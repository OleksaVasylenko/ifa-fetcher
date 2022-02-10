import contextlib
import os
import pathlib
import socket
import threading
import typing

import pytest
import werkzeug

tests_dir = pathlib.Path(os.path.dirname(__file__))
files_dir = tests_dir / "files"


@pytest.fixture
def ifa_aqua_response_html() -> str:
    return (files_dir / "aqua_canonical_response.html").read_text()


@pytest.fixture
def ifa_empty_response_html() -> str:
    return (files_dir / "ifa_empty_response.html").read_text()


@pytest.fixture
def unused_tcp_port() -> int:
    with contextlib.closing(socket.socket(type=socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class IFAServer:
    HOST = "localhost"
    SCHEME = "http://"

    def __init__(self, port: int):
        self._port = port
        self._server = werkzeug.serving.make_server(self.HOST, port, self)
        self._thread = threading.Thread(target=self._server.serve_forever)

        self.incoming_requests = []
        self.url = f"{self.SCHEME}{self.HOST}:{port}/"

    def start(self) -> None:
        self._thread.start()

    def __call__(self, environ: dict, start_response: typing.Callable):
        request = werkzeug.Request(environ)
        self.incoming_requests.append(request)
        response = werkzeug.Response("Hello_world")
        return response(environ, start_response)

    def stop(self) -> None:
        self._server.shutdown()
        self._server = None
        self._thread.join()


@pytest.fixture
def ifa_server(unused_tcp_port: int) -> None:
    server = IFAServer(unused_tcp_port)
    server.start()
    yield server
    server.stop()
