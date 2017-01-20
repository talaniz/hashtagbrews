from selenium import webdriver
from selenium.webdriver.support.select import Select

from .base import FunctionalTest


class SimpleHopSearchTest(FunctionalTest):

    def test_user_can_search_hops_page(self):
        """
        Test to verify that user can search the hops page for a record.

        User performs the following steps to complete the test:
                * Navigate to the hops page
                * Add a record in the hops table
                * Find the search field and populate a hops name
                * Click submit
                * Search the table to ensure that the record is present
        :return:
        """

        # Josh wants to visit the homebrew materials database to test the
        # search functionality
        self.browser.get(self.live_server_url)
        self.browser.implicitly_wait(5)

        beerdb_link = self.browser.find_element_by_id('beerdb').text

        self.assertEqual(beerdb_link, 'Homebrew Database')

        # He's redirected to the Homebrew Materials Database and
        # sees this listed in the title and the body of the page
        beerdb_link = self.browser.find_element_by_id('beerdb')

        beerdb_link.click()

        self.browser.implicitly_wait(5)
        page_heading = self.browser.find_element_by_tag_name('h1')

        self.assertIn("Homebrew Materials Database", page_heading.text)

        # He decides to try hops, clicks the Hops link and  is
        # redirected to the hops page.
        hops_link = self.browser.find_element_by_link_text('Hops')

        hops_link.click()
        self.browser.implicitly_wait(5)

        page_heading = self.browser.find_element_by_tag_name('h1').text

        self.assertIn(page_heading, 'Hops')

        # He finds the Add Hops button and clicks, a modal
        # form appears and he enters in a new hops name
        self.browser.find_element_by_id("add_hops").click()

        self.browser.implicitly_wait(6)

        # He enters the information into the form and clicks submit.
        inputbox = self.browser.find_element_by_id('new_hops')
        inputbox.send_keys('Amarillo')

        inputbox = self.browser.find_element_by_id('min_alpha_acid')
        inputbox.send_keys('8.52')

        inputbox = self.browser.find_element_by_id('max_alpha_acid')
        inputbox.send_keys('11.33')

        select = Select(self.browser.find_element_by_id('id_country'))
        select.select_by_visible_text('United States')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Good over all aroma and bittering hops')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)

        # He adds a second hop record that comes to mind
        self.browser.find_element_by_id("add_hops").click()

        self.browser.implicitly_wait(6)

        # He enters the information into the form and clicks submit.
        inputbox = self.browser.find_element_by_id('new_hops')
        inputbox.send_keys('Northern')

        inputbox = self.browser.find_element_by_id('min_alpha_acid')
        inputbox.send_keys('12.00')

        inputbox = self.browser.find_element_by_id('max_alpha_acid')
        inputbox.send_keys('15.00')

        select = Select(self.browser.find_element_by_id('id_country'))
        select.select_by_visible_text('United States')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Similar to Amarillo, good flavor')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)

        # He adds a second hop record that comes to mind
        self.browser.find_element_by_id("add_hops").click()

        self.browser.implicitly_wait(6)

        # He enters the information into the form and clicks submit.
        inputbox = self.browser.find_element_by_id('new_hops')
        inputbox.send_keys('Century')

        inputbox = self.browser.find_element_by_id('min_alpha_acid')
        inputbox.send_keys('9.00')

        inputbox = self.browser.find_element_by_id('max_alpha_acid')
        inputbox.send_keys('13.00')

        select = Select(self.browser.find_element_by_id('id_country'))
        select.select_by_visible_text('Czech Republic')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Good flavoring hops')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)

        # He sees the search bar and enters the name of his hops to see if it will
        # appear and clicks submit
        inputbox = self.browser.find_element_by_id('query')
        inputbox.send_keys('Amarillo')

        submit_button = self.browser.find_elements_by_id('submit')[3]
        submit_button.click()
        self.browser.implicitly_wait(6)

        # He sees the search bar and enters the name of his hops to see if it will
        # appear and clicks submit
        inputbox = self.browser.find_element_by_id('query')
        inputbox.send_keys('Amarillo')

        submit_button = self.browser.find_elements_by_id('submit')[3]
        submit_button.click()
        self.browser.implicitly_wait(6)

        # The page redirects and he sees the table wih the name of the hops
        # He can see the homepage only with hop records that match his search
        self.find_text_in_table('Amarillo')
        self.find_text_in_table('8.52')
        self.find_text_in_table('11.33')
        self.find_text_in_table('USA')
        self.find_text_in_table('Good over all aroma and bittering hops')

        self.find_text_in_table('Northern')
        self.find_text_in_table('12.0')
        self.find_text_in_table('15.0')
        self.find_text_in_table('USA')
        self.find_text_in_table('Similar to Amarillo, good flavor')

        self.find_text_not_in_table('Century')
        self.find_text_not_in_table('9.0')
        self.find_text_not_in_table('13.0')
        self.find_text_not_in_table('CZE')
        self.find_text_not_in_table('Good flavoring hops')

        # Satisfied, he closes his browser and brews some beer
