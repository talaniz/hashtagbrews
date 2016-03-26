from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.set_window_size(1750, 1000)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def find_text_in_hops_table(self, text):
        table = self.browser.find_element_by_id("hops_list_table")
        rows = table.find_elements_by_tag_name('td')
        self.assertIn(text, [row.text for row in rows])