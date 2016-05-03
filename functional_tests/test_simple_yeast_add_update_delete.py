from selenium import webdriver
from selenium.webdriver.support.select import Select

from .base import FunctionalTest


class NewYeastVisitorTest(FunctionalTest):
    """
    Simulation of a first time user adding yeast records

    * Note: View[Model]Visitor tests could use a helper function to navigate through the first 2 pages at this point
    """

    def test_user_can_navigate_to_yeast_page_and_save_record(self):
        """
        User performs the following tasks to add yeast record:
                * Navigate to site index
                * Navigate to homebrew database page
                * Select 'Yeasts' & redirect to yeasts main page
                * Click on modal 'Add Yeast', fill in form & submit
                * Check for submitted record on yeasts page
                * Quite browser, reopen yeasts main page and re-check for record

                :return: pass or fail
        """

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

        select = Select(self.browser.find_element_by_id('flocculation'))
        select.select_by_visible_text('Medium')

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

    def test_user_can_update_yeast_record(self):
        """
        User performs the following tasks to update yeast record:
                * Navigate to yeasts
                * Select 'Yeasts' & redirect to yeasts main page
                * Click on modal 'Add Yeast', fill in form & submit
                * Check for submitted record on yeasts page
                * Click on yeast name, change field name in modal, save
                * Check yeasts page to make sure record was successfully update

                :return: pass or fail
        """

        # John has decided to contribute to the open source homebrew database
        # He navigates to the yeasts page (Kevin showed him), and selects add yeasts
        grain_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/yeasts')
        self.browser.get(grain_live_server_url)

        self.browser.find_element_by_id("add_yeasts").click()

        self.browser.implicitly_wait(6)

        # He enters the information into the form and clicks submit.
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

        select = Select(self.browser.find_element_by_id('flocculation'))
        select.select_by_visible_text('Medium')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Well balanced.')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        # He closes out his browser, but then realizes that he's made a mistake.
        grains_page = self.browser.current_url
        self.browser.refresh()
        self.browser.quit()

        # The grain name wasn't 'American Ale 1056' it was 'WLP080 CREAM ALE YEAST BLEND'.
        # He decides to go back and update the record
        self.browser = webdriver.Firefox()
        self.browser.get(grains_page)

        self.browser.implicitly_wait(6)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(header_text, 'Yeasts')

        # He sees the link for the yeast record he just entered
        # and he clicks on it, a bootstrap modal form with the information pops up
        self.browser.find_element_by_link_text('American Ale 1056').click()
        self.browser.implicitly_wait(6)

        # He changes the grain name from Carared to Chocolate Pale and clicks submit.
        # He's redirected back to the grains list page and can see the change updated in the table
        inputbox = self.browser.find_element_by_id('update').find_element_by_id('name')

        inputbox.clear()
        inputbox.send_keys('WLP080 CREAM ALE YEAST BLEND')

        submit_button = self.browser.find_element_by_id('update').find_element_by_id('submit')
        submit_button.click()

        table = self.browser.find_element_by_id('list_table')
        rows = table.find_elements_by_tag_name('td')

        self.assertIn('WLP080 CREAM ALE YEAST BLEND', [row.text for row in rows])
        self.assertNotIn('American Ale 1056', [row.text for row in rows])
