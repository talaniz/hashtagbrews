from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command

from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):
    """
    Base class for functional tests, sublcasses StaticLiveServerTestCase
    """

    def setUp(self):
        """
        Basic unit test setup method
                :return: none
        """

        call_command('push_hop_to_index')

        self.browser = webdriver.Firefox()
        self.browser.set_window_size(1750, 1000)

    def tearDown(self):
        """
        Basic tear down setup method
                :return: none
        """

        call_command('push_hop_to_index')
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
