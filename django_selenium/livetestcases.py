from django.test import LiveServerTestCase

from django_selenium.testcases import MyDriver
from django_selenium import settings


class SeleniumLiveTestCase(LiveServerTestCase):
    """Selenium TestCase for django 1.4 with custom MyDriver"""

    @classmethod
    def setUpClass(cls):
        cls.driver = MyDriver()
        super(SeleniumLiveTestCase, cls).setUpClass()

    def setUp(self):
        self.driver.live_server_url = self.live_server_url

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(SeleniumLiveTestCase, cls).tearDownClass()
