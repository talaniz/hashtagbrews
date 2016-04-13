from selenium import webdriver
from selenium.webdriver.support.select import Select

from .base import FunctionalTest


class NewGrainVisitorTest(FunctionalTest):

    def test_user_can_navigate_to_grains_page_and_save_grains_record(self):
        # Kevin wants to contribute to the Open Source Homebrew Database
        # He navigates to the homepage and clicks the link to navigate
        # to the Open Source Homebrew database.
        self.browser.get(self.live_server_url)
        self.browser.implicitly_wait(5)

        beerdb_link = self.browser.find_element_by_id('beerdb').text

        self.assertEqual(beerdb_link, 'Homebrew Database')

        # He's redirected to the Homebrew Materials Database and
        # sees this listed in the title and the body of the page
        beerdb_link = self.browser.find_element_by_id('beerdb')

        beerdb_link.click()

        page_heading = self.browser.find_element_by_tag_name('h1')

        self.assertIn("Homebrew Materials Database", page_heading.text)

        # Kevin is presented with 3 categories to choose from: Hops, Grains and Yeasts
        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertIn('Hops', page_text)
        self.assertIn('Grains', page_text)
        self.assertIn('Yeasts', page_text)

        # He decides to try grains, clicks the Hops link and  is
        # redirected to the grains page.
        hops_link = self.browser.find_element_by_link_text('Grains')
        hops_link.click()

        page_heading = self.browser.find_element_by_tag_name('h1').text

        self.assertIn(page_heading, 'Grains')

        # He finds the Add Grain button and clicks, a modal
        # form appears and he enters in a new hops name
        self.browser.find_element_by_id("add_grain").click()

        self.browser.implicitly_wait(6)

        # He enters the information into the form and clicks submit.
        inputbox = self.browser.find_element_by_id('name')
        inputbox.send_keys('Carared')

        inputbox = self.browser.find_element_by_id('degrees_lovibond')
        inputbox.send_keys('1.5')

        inputbox = self.browser.find_element_by_id('specific_gravity')
        inputbox.send_keys('1.20')

        select = Select(self.browser.find_element_by_id('grain_type'))
        select.select_by_visible_text('Grain')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Red amber color')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)

        # He can see the homepage with his hop record in the table
        self.find_text_in_table('Carared')
        self.find_text_in_table('1.50')
        self.find_text_in_table('1.200')
        self.find_text_in_table('Red amber color')

        # Satisfied, he closes his browser and brews some beer
        grains_page = self.browser.current_url
        self.browser.refresh()
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Kevin wonders if the site really saved his record.
        # He opens up the browser to the grains main page and checks
        # to make sure the information he entered is still here
        self.browser.get(grains_page)

        self.find_text_in_table('Carared')
        self.find_text_in_table('1.50')
        self.find_text_in_table('1.200')
        self.find_text_in_table('Red amber color')

        # Satisfied once again, he returns to his boil.
