import socket
from django.core.servers import basehttp
from django.core.handlers.wsgi import WSGIHandler
from django.contrib.staticfiles.handlers import StaticFilesHandler

import threading
from django_selenium import settings

try:
    from django.core.servers.basehttp import WSGIServerException \
                                             as wsgi_exec_error
except ImportError:
    import socket
    wsgi_exec_error = socket.error                                            

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
        self._activate_event = threading.Event()
        self._ready_event = threading.Event()
        self._error = None
        super(TestServerThread, self).__init__()

    def run(self):
        try:
            handler = StaticFilesHandler(WSGIHandler())
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
        except wsgi_exec_error as e:
            self.error = e
            self._start_event.set()
            return
        self._activate_event.set()
        # Loop until we get a stop event.
        while not self._stop_event.is_set():
            if self._activate_event.wait(5):
                httpd.handle_request()
            self._ready_event.set()

    def stop(self, timeout=None):
        """Stop the thread and wait for it to finish."""
        self._stop_event.set()
        self.join(timeout)

    def activate(self):
        """Activate the server and wait until it changes the status."""
        self._activate_event.set()
        self._ready_event.clear()
        if not self._ready_event.wait(settings.SELENIUM_TEST_SERVER_TIMEOUT):
            raise Exception('Test server hung. Timed out after %i seconds' % settings.SELENIUM_TEST_SERVER_TIMEOUT)

    def deactivate(self):
        """Deactivate the server and wait until it finishes processing requests."""
        self._activate_event.clear()
        self._ready_event.clear()
        if not self._ready_event.wait(settings.SELENIUM_TEST_SERVER_TIMEOUT):
            raise Exception('Test server hung. Timed out after %i seconds' % settings.SELENIUM_TEST_SERVER_TIMEOUT)


def get_test_server():
    """ TestServer lazy initialization with singleton"""

    #TODO: make this lazy initialization thread-safe
    if '__instance' not in globals():
        server_thread = TestServerThread(settings.SELENIUM_TESTSERVER_HOST, settings.SELENIUM_TESTSERVER_PORT)
        server_thread.start()
        server_thread._start_event.wait()
        if server_thread._error:
            raise server_thread._error
        globals()['__instance'] = server_thread

    return globals()['__instance']
