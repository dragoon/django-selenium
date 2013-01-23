from django.core.urlresolvers import reverse
from django_selenium.livetestcases import SeleniumLiveTestCase

class MyTestCase(SeleniumLiveTestCase):

    def test_home(self):
        self.driver.open_url(reverse('home'))
        import time
        # Sleep to check browser is opened
        time.sleep(10)
        self.failUnless(self.driver.is_text_present('Test Page'))
        self.assertEquals(self.driver.get_title(), 'Home')
