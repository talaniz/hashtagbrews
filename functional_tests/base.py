from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class FunctionalTest(StaticLiveServerTestCase):
    """
    Base class for functional tests, sublcasses StaticLiveServerTestCase
    """

    def setUp(self):
        """
        Basic unit test setup method
                :return: none
        """

        self.user = User.objects.create_user(username='john75', email="john@example.com",
                                             password='sally75')

        call_command('push_hop_to_index')
        call_command('push_grain_to_index')
        call_command('push_yeast_to_index')

        self.browser = webdriver.Firefox()
        self.browser.set_window_size(1750, 1000)

    def tearDown(self):
        """
        Basic tear down setup method
                :return: none
        """

        call_command('push_hop_to_index')
        call_command('push_grain_to_index')
        call_command('push_yeast_to_index')

        self.browser.refresh()
        self.browser.quit()

    def find_text_in_table(self, text):
        """
        Helper function to find text in html tables. Only searches tables with 'list_table' html id
                :param text: the text to find in the table
                :return: pass or fail
        """

        table = self.browser.find_element_by_id("list_table")
        rows = table.find_elements_by_tag_name('td')
        self.assertIn(text, [row.text for row in rows])

    def find_text_not_in_table(self, text):
        """
        Helper function to find text in html tables. Only searches tables with 'list_table' html id
                :param text: the text to find in the table
                :return: pass or fail
        """

        table = self.browser.find_element_by_id("list_table")
        rows = table.find_elements_by_tag_name('td')
        self.assertNotIn(text, [row.text for row in rows])

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=60).until(
            lambda b: b.find_element_by_id(element_id)
        )

    def auth_client(self, url):
        """Authenticate the client and return them to the url."""
        self.client.login(username='john75', password='sally75')
        cookie = self.client.cookies['sessionid']
        self.browser.get(url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh() #need to update page for logged in user
