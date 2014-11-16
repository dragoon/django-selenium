from django.conf import settings

# Specify the selenium test runner
SELENIUM_TEST_RUNNER = getattr(settings, 'SELENIUM_TEST_RUNNER',
                             'django_selenium.selenium_runner.SeleniumTestRunner')

SELENIUM_TIMEOUT = getattr(settings, 'SELENIUM_TIMEOUT', 120)
SELENIUM_DRIVER_TIMEOUT = getattr(settings, 'SELENIUM_DRIVER_TIMEOUT', 10)
# Specify max waiting time for server to finish processing request and deactivates
SELENIUM_TEST_SERVER_TIMEOUT = getattr(settings, 'SELENIUM_TEST_SERVER_TIMEOUT', 300)

#------------------ LOCAL ----------------------------------
SELENIUM_TESTSERVER_HOST = getattr(settings, 'SELENIUM_TESTSERVER_HOST', 'localhost')
SELENIUM_TESTSERVER_PORT = getattr(settings, 'SELENIUM_TESTSERVER_PORT', 8011)
SELENIUM_HOST = getattr(settings, 'SELENIUM_HOST', None)
SELENIUM_PORT = getattr(settings, 'SELENIUM_PORT', 4444)

SELENIUM_DISPLAY = getattr(settings, 'SELENIUM_DISPLAY', ':0')
# Set the drivers that you want to run your tests against
SELENIUM_DRIVER = getattr(settings, 'SELENIUM_DRIVER', 'Firefox')
SELENIUM_DRIVER_OPTS = getattr(settings, 'SELENIUM_DRIVER_OPTS', dict())
#------------------------------------------------------------

#----------------- REMOTE ------------------------------------
# YOU SHOULD SET THESE IN YOUR LOCAL SETTINGS FILE
# Path to selenium-server JAR,
# for example: "/home/dragoon/myproject/selenium-server/selenium-server.jar"
SELENIUM_PATH=getattr(settings, 'SELENIUM_PATH', None)
SELENIUM_CAPABILITY =  getattr(settings, 'SELENIUM_CAPABILITY', 'FIREFOX')
#SELENIUM_DRIVER = 'Remote'
#SELENIUM_HOST = getattr(settings, 'SELENIUM_HOST', 'selenium-hub.example.com')
#SELENIUM_TESTSERVER_HOST = getattr(settings, 'SELENIUM_TESTSERVER_HOST', '0.0.0.0')
#------------------------------------------------------------
