from django.core.urlresolvers import reverse
from django_selenium.livetestcases import SeleniumLiveTestCase


class MyTestCase(SeleniumLiveTestCase):

    def test_home(self):
        self.driver.open_url(reverse('main'))
        self.assertEquals(self.driver.get_title(), 'Sample Test Page')
        self.driver.type_in('input#id_query', 'search something')
        self.driver.click('.form-search button[type="submit"]')

        self.assertEquals(self.driver.get_text('#success'), 'SUCCESS')
