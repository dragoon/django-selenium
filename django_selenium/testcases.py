from functools import wraps
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import os

from django.db import transaction
from django.core.urlresolvers import reverse
from django.test import TransactionTestCase
from django.utils.html import strip_tags

from django_selenium import settings, selenium_server


def wait(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        i = settings.SELENIUM_DRIVER_TIMEOUT
        if 'timeout' in kwargs:
            i = kwargs.pop('timeout')
        res = func(self, *args, **kwargs)
        while not res and i:
            time.sleep(1)
            res = func(self, *args, **kwargs)
            i -= 1
        return res
    return wrapper


class SeleniumElement(object):

    def __init__(self, elements, selector):
        """Keep selector for key errors"""
        self.elements = elements
        self.selector = selector

    def __getattribute__(self, name):
        """
        Pass ``__getattribute__`` directly to the first array element.
        """
        try:
            attr = object.__getattribute__(self, 'elements')[0].__getattribute__(name)
        except IndexError:
            raise NoElementException(u'No elements found for selector: {0}'\
                .format(object.__getattribute__(self, 'selector')))
        return attr

    def __getitem__(self, key):
        """Return item from the internal sequence, bypassing ``__getattribute__``"""
        return object.__getattribute__(self, 'elements')[key]


class NoElementException(Exception):
    pass


class MyDriver(object):
    def __init__(self):
        driver = getattr(webdriver, settings.SELENIUM_DRIVER, None)
        assert driver, "settings.SELENIUM_DRIVER contains non-existing driver"
        driver_opts = getattr(settings, "SELENIUM_DRIVER_OPTS", dict())
        if driver is webdriver.Remote:
            if isinstance(settings.SELENIUM_CAPABILITY, dict):
                capability = settings.SELENIUM_CAPABILITY
            else:
                capability = getattr(webdriver.DesiredCapabilities, settings.SELENIUM_CAPABILITY, None)
                assert capability, 'settings.SELENIUM_CAPABILITY contains non-existing capability'
            self.driver = driver('http://%s:%d/wd/hub' % (settings.SELENIUM_HOST, settings.SELENIUM_PORT), capability, **driver_opts)
        else:
            self.driver = driver(**driver_opts)
        self.live_server_url = 'http://%s:%s' % (settings.SELENIUM_TESTSERVER_HOST , str(settings.SELENIUM_TESTSERVER_PORT))
        self.text = ''

    def __getattribute__(self, name):
        try:
            attr = object.__getattribute__(self, name)
        except AttributeError:
            attr = self.driver.__getattribute__(name)
        return attr

    def _wait_for_page_source(self):
        try:
            page_source = self.page_source
            time.sleep(1)
            while page_source != self.page_source:
                page_source = self.page_source
                time.sleep(1)
            self.update_text()
        except WebDriverException:
            pass

    def authorize(self, username, password):
        self.open_url(reverse('login'))
        self.type_in("#id_username", username)
        self.type_in("#id_password", password)
        self.click("#login-form [type='submit']")

    def update_text(self):
        """
        Update text content of the current page.
        Use in case you cannot find text that is actually present on the page.
        """
        self.text = strip_tags(unicode(self.page_source))

    def open_url(self, url):
        """Open the specified url and wait until page source is fully loaded."""
        self.get('%s%s' % (self.live_server_url, url))
        self._wait_for_page_source()

    def click(self, selector):
        """
        :param selector: CSS selector of the element to be clicked on.
        Performs click on the specified CSS selector.
        Also refreshes page text.
        """
        self.find(selector).click()
        self._wait_for_page_source()

    def click_and_wait(self, selector, newselector):
        """
        :param selector: CSS selector of the element to be clicked on.
        :param newselector: CSS selector of the new element to wait for.
        Calls click function and then waits for element presense on the updated page.
        """
        self.click(selector)
        return self.wait_element_present(newselector)

    def is_element_present(self, selector):
        """Check if one or more elements specified by CSS selector are present on the current page."""
        return len(self.find_elements_by_css_selector(selector)) > 0

    def is_text_present(self, text):
        """Check if specified text is present on the current page."""
        return text in self.text

    def get_alert_text(self):
        """
        Get text of the current alert and close it.
        :returns: alert text
        """
        alert = self.switch_to_alert()
        # Selenium can return either dict or text,
        # TODO: Need to investigate why
        try:
            text = alert.text['text']
        except TypeError:
            text = alert.text
        alert.dismiss()
        self.switch_to_default_content()
        self.update_text()
        return text

    def get_text(self, selector):
        return self.find(selector).text

    def drop_image(self, file_path, droparea_selector, append_to):
        """Drop image to the element specified by selector"""
        self.execute_script("file_input = window.$('<input/>').attr({id: 'file_input', type:'file'}).appendTo('" + append_to + "');")
        self.find('#file_input').send_keys(os.path.join(os.getcwd(), file_path))
        self.execute_script('fileList = Array();fileList.push(file_input.get(0).files[0]);')
        self.execute_script("e = $.Event('drop'); e.originalEvent = {dataTransfer : { files : fileList } }; $('" + droparea_selector + "').trigger(e);")
        self.execute_script("$('#file_input').remove()")

    @wait
    def wait_for_text(self, selector, text):
        return text in self.find(selector).text

    @wait
    def wait_for_visible(self, selector, visible=True):
        return self.find(selector).is_displayed() == visible

    @wait
    def wait_element_present(self, selector, present=True):
        return self.is_element_present(selector) == present

    def get_title(self):
        return self.title

    def get_value(self, selector):
        return self.find(selector).get_attribute('value')

    def find(self, cssselector):
        """
        :returns: element specified by a CSS selector ``cssselector``
        :rtype: SeleniumElement
        """
        return SeleniumElement(self.find_elements_by_css_selector(cssselector), cssselector)

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
            attr = object.__getattribute__(self, 'driver').__getattribute__(name)
        return attr

    def _fixture_setup(self):
        test_server = selenium_server.get_test_server()
        test_server.deactivate()
        transaction.commit_unless_managed()
        transaction.enter_transaction_management()
        transaction.managed(True)
        super(SeleniumTestCase, self)._fixture_setup()
        transaction.commit()
        transaction.leave_transaction_management()
        test_server.activate()

    def setUp(self):
        import socket
        socket.setdefaulttimeout(settings.SELENIUM_TIMEOUT)
        self.driver = MyDriver()

    def tearDown(self):
        self.driver.quit()
