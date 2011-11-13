from django_jenkins.runner import CITestSuiteRunner
from django_selenium.selenium_runner import SeleniumTestRunner

class JenkinsTestRunner(CITestSuiteRunner, SeleniumTestRunner):
    def __init__(self, **kwargs):
        super(MyJenkinsRunner, self).__init__(**kwargs)
        self.selenium = True

    def build_suite(self, test_labels, **kwargs):
        suite = SeleniumTestRunner.build_suite(self, test_labels, **kwargs)
        return suite

    def run_tests(self, test_labels, extra_tests=None, **kwargs):

        self._start_selenium()
        results = super(MyJenkinsRunner, self).run_tests(test_labels, extra_tests, **kwargs)
        self._stop_selenium()

        return results
