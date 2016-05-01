from selenium import webdriver
from selenium.webdriver.support.select import Select

from .base import FunctionalTest


class NewYeastVisitor(FunctionalTest):

    def test_user_can_navigate_to_yeast_page_and_save_record(self):
        # Jerry has heard about the Homebrew Database site and wants to contribute
        # He navigates to the homepage and clicks the link to go to the Homebrew Database
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

        # He decides to try yeasts, clicks the Yeasts link and  is
        # redirected to the yeasts page.
        yeast_link = self.browser.find_element_by_link_text('Yeasts')
        yeast_link.click()

        page_heading = self.browser.find_element_by_tag_name('h1').text

        self.assertIn(page_heading, 'Yeasts')

        # He finds the Add Yeast button and clicks, a modal
        # form appears and he enters in a new yeast name
        self.browser.find_element_by_id("add_yeasts").click()

        self.browser.implicitly_wait(6)

        # He enters the information into the form and clicks submit
        inputbox = self.browser.find_element_by_id('name')
        inputbox.send_keys('American Ale 1056')

        select = Select(self.browser.find_element_by_id('lab'))
        select.select_by_visible_text('Wyeast')

        select = Select(self.browser.find_element_by_id('yeast_type'))
        select.select_by_visible_text('Ale')

        select = Select(self.browser.find_element_by_id('yeast_form'))
        select.select_by_visible_text('Liquid')

        inputbox = self.browser.find_element_by_id('min_temp')
        inputbox.send_keys('60')

        inputbox = self.browser.find_element_by_id('max_temp')
        inputbox.send_keys('72')

        inputbox = self.browser.find_element_by_id('attenuation')
        inputbox.send_keys('75')

        inputbox = self.browser.find_element_by_id('flocculation')
        inputbox.send_keys('Medium')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Well balanced.')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        self.browser.implicitly_wait(6)

        # He can see the yeasts main page with his record in the table
        self.find_text_in_table('American Ale 1056')
        self.find_text_in_table('Wyeast')
        self.find_text_in_table('Ale')
        self.find_text_in_table('Liquid')
        self.find_text_in_table('60')
        self.find_text_in_table('72')
        self.find_text_in_table('75')
        self.find_text_in_table('Medium')
        self.find_text_in_table('Well balanced.')

        # Satisfied, he closes his browser and brews some beer
        yeast_page = self.browser.current_url
        self.browser.refresh()
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Kevin wonders if the site really saved his record.
        # He opens up the browser to the grains main page and checks
        # to make sure the information he entered is still here
        self.browser.get(yeast_page)

        self.find_text_in_table('American Ale 1056')
        self.find_text_in_table('Wyeast')
        self.find_text_in_table('Ale')
        self.find_text_in_table('Liquid')
        self.find_text_in_table('60')
        self.find_text_in_table('72')
        self.find_text_in_table('75')
        self.find_text_in_table('Medium')
        self.find_text_in_table('Well balanced.')

        # Satisfied, he once again returns to his boil
