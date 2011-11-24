import socket
from django.core.servers import basehttp
from django.core.handlers.wsgi import WSGIHandler

import threading

class StoppableWSGIServer(basehttp.WSGIServer):
    """WSGIServer with short timeout"""

    def server_bind(self):
        """Sets timeout to 1 second."""
        basehttp.WSGIServer.server_bind(self)
        self.socket.settimeout(1)

    def get_request(self):
        """Checks for timeout when getting request."""
        try:
            sock, address = self.socket.accept()
            sock.settimeout(None)
            return (sock, address)
        except socket.timeout:
            raise

class TestServerThread(threading.Thread):
    """Thread for running a http server."""

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self._start_event = threading.Event()
        self._stop_event = threading.Event()
        self._error = None
        super(TestServerThread, self).__init__()

    def run(self):
        try:
            handler = basehttp.AdminMediaHandler(WSGIHandler())
            def test_app(environ, start_response):
                if environ['REQUEST_METHOD'] == 'HEAD':
                    start_response('200 OK', [])
                    return ''
                if environ['PATH_INFO'] == '/favicon.ico':
                    start_response('404 Not Found', [])
                    return ''
                return handler(environ, start_response)
            server_address = (self.address, self.port)
            httpd = StoppableWSGIServer(server_address, basehttp.WSGIRequestHandler)
            httpd.set_app(test_app)
            self._start_event.set()
        except basehttp.WSGIServerException, e:
            self.error = e
            self._start_event.set()
            return

        # Loop until we get a stop event.
        while not self._stop_event.is_set():
            httpd.handle_request()

    def stop(self, timeout=None):
        """Stop the thread and wait for it to finish."""
        self._stop_event.set()
        self.join(timeout)

def start_test_server(address='localhost', port=8000):
    server_thread = TestServerThread(address, port)
    server_thread.start()
    server_thread._start_event.wait()
    if server_thread._error:
        raise server_thread._error
    return server_thread
