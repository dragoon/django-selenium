from django.dispatch import receiver
from django_jenkins.runner import CITestSuiteRunner
from django_jenkins.signals import build_suite
from django_selenium.selenium_runner import SeleniumTestRunner

class JenkinsTestRunner(CITestSuiteRunner, SeleniumTestRunner):
    def __init__(self, **kwargs):
        super(JenkinsTestRunner, self).__init__(**kwargs)
        self.selenium = True

    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        # args and kwargs saved in instance to use in the signal below
        self.test_labels = test_labels
        self.build_suite_kwargs = kwargs
        suite = CITestSuiteRunner.build_suite(self, test_labels, extra_tests, **kwargs)
        return suite

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        results = super(JenkinsTestRunner, self).run_tests(test_labels, extra_tests, **kwargs)
        return results


@receiver(build_suite)
def add_selenium_tests(sender, suite, **kwargs):
    ''' Add the selenium test under Jenkins environment '''
    sel_suite = sender._get_seltests(sender.test_labels, **sender.build_suite_kwargs)
    suite.addTest(sel_suite)

