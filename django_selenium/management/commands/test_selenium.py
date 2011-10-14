from optparse import make_option
import sys

from django.conf import settings
from django.core.management.commands import test
from django.test.utils import get_runner

from django_selenium import settings as selenium_settings


class Command(test.Command):
    # TODO: update when django 1.4 is out, it will have custom options available
    option_list = test.Command.option_list + (
        make_option('--selenium', action='store_true', dest='selenium', default=False,
            help='Run selenium tests during test execution\n'
                 '(requires access to 4444 and $SELENIUM_TESTSERVER_PORT ports, java and running X server'),
        make_option('--selenium-only', action='store_true', dest='selenium_only', default=False,
            help='Run only selenium tests (implies --selenium)')
    )

    def handle(self, *test_labels, **options):

        verbosity = int(options.get('verbosity', 1))
        interactive = options.get('interactive', True)
        failfast = options.get('failfast', False)
        selenium = options.get('selenium', False)
        selenium_only = options.get('selenium_only', False)
        if selenium_only:
            selenium = True

        TestRunner = get_runner(settings)
        test_runner = TestRunner(verbosity=verbosity, interactive=interactive, failfast=failfast,
                                 selenium=selenium, selenium_only=selenium_only)
        failures = test_runner.run_tests(test_labels)
        if failures:
            sys.exit(bool(failures))
