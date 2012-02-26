import os
import socket
import subprocess
import time
import signal
import unittest

from django_selenium import settings
from django.test.simple import reorder_suite
from django.test.testcases import TestCase
from django_selenium.selenium_server import start_test_server

try:
    from django.test.simple import DjangoTestSuiteRunner
except ImportError:
    msg = """

    django-selenium requires django 1.2+.
    """
    raise ImportError(msg)

SELTEST_MODULE = 'seltests'

def wait_until_connectable(port, timeout=120):
    """Blocks until the specified port is connectable."""

    def is_connectable(port):
        """Tries to connect to the specified port."""
        try:
            socket_ = socket.create_connection(("127.0.0.1", port), 1)
            socket_.close()
            return True
        except socket.error:
            return False

    count = 0
    while not is_connectable(port):
        if count >= timeout:
            return False
        count += 5
        time.sleep(5)
    return True

class SeleniumTestRunner(DjangoTestSuiteRunner):
    """
    Test runner with Selenium support
    """

    def __init__(self, **kwargs):
        super(SeleniumTestRunner, self).__init__(**kwargs)
        self.selenium = kwargs.get('selenium')
        self.selenium_only = kwargs.get('selenium_only')

        self.test_server = None
        self.selenium_server = None

    def _is_start_selenium_server(self):
        return bool((settings.SELENIUM_DRIVER == 'Remote') and settings.SELENIUM_PATH)

    def build_suite(self, test_labels, *args, **kwargs):
        suite = unittest.TestSuite()

        if not self.selenium_only:
            suite = super(SeleniumTestRunner, self).build_suite(test_labels, *args, **kwargs)

        if self.selenium:
            # Hack to exclude doctests from selenium-only, they are already present
            from django.db.models import get_app
            if test_labels:
                for label in test_labels:
                    if not '.' in label:
                        app = get_app(label)
                        setattr(app, 'suite', unittest.TestSuite)


            sel_suite = self._get_seltests(test_labels, *args, **kwargs)
            suite.addTest(sel_suite)

        return reorder_suite(suite, (TestCase,))

    def _get_seltests(self, *args, **kwargs):
        # Add tests from seltests.py modules
        import django.test.simple
        orig_test_module = django.test.simple.TEST_MODULE
        django.test.simple.TEST_MODULE = SELTEST_MODULE
        try:
            sel_suite = DjangoTestSuiteRunner.build_suite(self, *args, **kwargs)
        finally:
             django.test.simple.TEST_MODULE = orig_test_module

        return sel_suite


    def _start_selenium(self):
        if self.selenium:

            # Set display variable
            os.environ['DISPLAY'] = settings.SELENIUM_DISPLAY
            # Start test server
            self.test_server = start_test_server(address=settings.SELENIUM_TESTSERVER_HOST, port=settings.SELENIUM_TESTSERVER_PORT)
            if self._is_start_selenium_server():
                # Start selenium server
                self.selenium_server = subprocess.Popen(('java -jar %s' % settings.SELENIUM_PATH).split())

                # Waiting for server to be ready
                if not wait_until_connectable(4444):
                    self.selenium_server.kill()
                    self.test_server.stop()
                    assert False, "selenium server does not respond"

    def _stop_selenium(self):
        if self.selenium:
            # Stop selenium server
            if self._is_start_selenium_server():
                selenium_server = self.selenium_server
                selenium_server.send_signal(signal.SIGINT)
                if selenium_server.poll() is None:
                    selenium_server.kill()
                    selenium_server.wait()
            # Stop test server
            if self.test_server:
                self.test_server.stop()

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        self._start_selenium()
        try:
            results = super(SeleniumTestRunner, self).run_tests(test_labels, extra_tests, **kwargs)
        finally:
            self._stop_selenium()

        return results
