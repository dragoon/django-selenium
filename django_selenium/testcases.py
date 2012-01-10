from functools import wraps
from selenium import webdriver
import time

from django.db import transaction
from django.core.urlresolvers import reverse
from django.test import TransactionTestCase
from django.utils.html import strip_tags

from django_selenium import settings

def wait(timeout=10):
    def inner_wait(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            i = timeout
            while not res and i:
                time.sleep(1)
                res = func(self, *args, **kwargs)
                i-=1
            return res
        return wrapper
    return inner_wait


class MyDriver(object):
    def __init__(self):
        driver = getattr(webdriver, settings.SELENIUM_DRIVER, None)
        assert driver, "settings.SELENIUM_DRIVER contains non-existing driver"
        if driver is webdriver.Remote:
            if isinstance(settings.SELENIUM_CAPABILITY, dict):
                capability = settings.SELENIUM_CAPABILITY
            else:
                capability = getattr(webdriver.DesiredCapabilities, settings.SELENIUM_CAPABILITY, None)
                assert capability, 'settings.SELENIUM_CAPABILITY contains non-existing capability'
            self.driver = driver('http://%s:%d/wd/hub' % (settings.SELENIUM_HOST, settings.SELENIUM_PORT), capability)
        else:
            self.driver = driver()
        self.testserver_host = settings.SELENIUM_TESTSERVER_HOST
        self.testserver_port = settings.SELENIUM_TESTSERVER_PORT
        self.text = ''

    def __getattribute__(self, name):
        try:
            attr = object.__getattribute__(self, name)
        except AttributeError:
            attr = self.driver.__getattribute__(name)
        return attr

    def _wait_for_page_source(self):
        page_source = self.page_source
        time.sleep(1)
        while page_source!=self.page_source:
            page_source = self.page_source
            time.sleep(1)
        self.update_text()

    def authorize(self, username, password):
        self.open_url(reverse('login'))
        self.type_in("#id_username", username)
        self.type_in("#id_password", password)
        self.click("#login-form input[type='submit']")

    def update_text(self):
        self.text = strip_tags(unicode(self.page_source))

    def open_url(self, url):
        self.get('http://%s:%d' % (self.testserver_host , self.testserver_port) + url)
        self._wait_for_page_source()

    def click(self, selector):
        """This function also refreshes page text"""
        self.find(selector).click()
        self._wait_for_page_source()

    def click_and_wait(self, selector, newselector):
        self.click(selector)
        res = self.find(newselector).is_displayed()
        return res

    def is_element_present(self, selector):
        return len(self.find_elements_by_css_selector(selector)) > 0

    def is_text_present(self, text):
        return text in self.text

    def get_alert_text(self):
        alert = self.switch_to_alert()
        # Selenium can return either dict or text,
        # TODO: Need to investigate why
        try:
            text = alert.text['text']
        except TypeError:
            text = alert.text
        alert.dismiss()
        self.switch_to_default_content()
        return text

    def get_text(self, selector):
        return self.find(selector).text

    @wait(timeout=10)
    def wait_for_text(self, selector, text):
        return text in self.find(selector).text

    @wait(timeout=10)
    def wait_for_visible(self, selector, visible=True):
        return self.find(selector).is_displayed() == visible

    def get_title(self):
        return self.title

    def get_value(self, selector):
        return self.find(selector).get_attribute('value')

    def find(self, cssselector):
        return self.find_element_by_css_selector(cssselector)

    def select(self, selector, value):
        self.click(selector + (" option[value='%s']" % value))

    def type_in(self, selector, text):
        elem = self.find(selector)
        elem.clear()
        elem.send_keys(text)

class SeleniumTestCase(TransactionTestCase):

    def __getattribute__(self, name):
        try:
            attr = object.__getattribute__(self, name)
        except AttributeError:
            attr = object.__getattribute__(self,'driver').__getattribute__(name)
        return attr

    def _fixture_setup(self):
        transaction.commit_unless_managed()
        transaction.enter_transaction_management()
        transaction.managed(True)
        super(SeleniumTestCase, self)._fixture_setup()
        transaction.commit()
        transaction.leave_transaction_management()

    def setUp(self):
        import socket
        socket.setdefaulttimeout(settings.SELENIUM_TIMEOUT)
        self.driver = MyDriver()
        self.driver.implicitly_wait(settings.SELENIUM_TIMEOUT)

    def tearDown(self):
        self.driver.quit()

