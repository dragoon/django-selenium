from django.conf import settings

# Specify the selenium test runner
SELENIUM_TEST_RUNNER = getattr(settings, 'SELENIUM_TEST_RUNNER',
                             'django_selenium.selenium_runner.SeleniumTestRunner')

SELENIUM_DISPLAY = getattr(settings, 'SELENIUM_DISPLAY', ':0')

# Path to selenium-server JAR
SELENIUM_PATH=getattr(settings, 'SELENIUM_PATH', None)

SELENIUM_TESTSERVER_PORT = getattr(settings, 'SELENIUM_TESTSERVER_PORT', 8011)

# Set the drivers that you want to run your tests against
SELENIUM_DRIVERS = getattr(settings, 'SELENIUM_DRIVERS', ('Firefox',))
