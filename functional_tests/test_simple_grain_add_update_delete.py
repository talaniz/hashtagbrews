from selenium import webdriver
from selenium.webdriver.support.select import Select

from .base import FunctionalTest


class NewGrainVisitorTest(FunctionalTest):

    def test_user_can_navigate_to_grains_page_and_save_grains_record(self):
        # Kevin wants to contribute to the Open Source Homebrew Database.
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

        # He decides to try grains, clicks the Grains link and  is
        # redirected to the grains page.
        grains_link = self.browser.find_element_by_link_text('Grains')
        grains_link.click()

        page_heading = self.browser.find_element_by_tag_name('h1').text

        self.assertIn(page_heading, 'Grains')

        # He finds the Add Grain button and clicks, a modal
        # form appears and he enters in a new grain name
        self.browser.find_element_by_id("add_grain").click()

        self.browser.implicitly_wait(6)

        # He enters the information into the form and clicks submit.
        inputbox = self.browser.find_element_by_id('name')
        inputbox.send_keys('Carared')

        inputbox = self.browser.find_element_by_id('degrees_lovibond')
        inputbox.send_keys('1.5')

        inputbox = self.browser.find_element_by_id('specific_gravity')
        inputbox.send_keys('1.20')

        select = Select(self.browser.find_element_by_id('id_grain_type'))
        select.select_by_visible_text('Grain')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Red amber color')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)

        # He can see the homepage with his grain record in the table
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

    def test_user_can_update_grain_record(self):
        # John has decided to contribute to the open source homebrew database
        # He navigates to the grains page (Kevin showed him), and selects add grains
        grain_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/grains')
        self.browser.get(grain_live_server_url)

        self.browser.find_element_by_id("add_grain").click()

        self.browser.implicitly_wait(6)

        # He enters the information into the form and clicks submit.
        inputbox = self.browser.find_element_by_id('name')
        inputbox.send_keys('Carared')

        inputbox = self.browser.find_element_by_id('degrees_lovibond')
        inputbox.send_keys('1.50')

        inputbox = self.browser.find_element_by_id('specific_gravity')
        inputbox.send_keys('11.00')

        select = Select(self.browser.find_element_by_id('id_grain_type'))
        select.select_by_visible_text('Grain')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Adds reddish brown color')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        # He closes out his browser, but then realizes that he's made a mistake.
        grains_page = self.browser.current_url
        self.browser.refresh()
        self.browser.quit()

        # The grain name wasn't 'Carared' it was 'Chocolate Paul'. He decides to go back and update the record
        self.browser = webdriver.Firefox()
        self.browser.get(grains_page)

        self.browser.implicitly_wait(6)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(header_text, 'Grains')

        # He sees the link for the Carared grain record he just entered
        # and he clicks on it, a bootstrap modal form with the information
        # pops up
        self.browser.find_element_by_link_text('Carared').click()
        self.browser.implicitly_wait(6)

        # He changes the grain name from Carared to Chocolate Pale and clicks submit.
        # He's redirected back to the grains list page and can see the change updated
        # in the table
        inputbox = self.browser.find_element_by_id('update').find_element_by_id('name')

        inputbox.clear()
        inputbox.send_keys('Chocolate Pale')

        submit_button = self.browser.find_element_by_id('update').find_element_by_id('submit')
        submit_button.click()

        table = self.browser.find_element_by_id('list_table')
        rows = table.find_elements_by_tag_name('td')

        self.assertIn('Chocolate Pale', [row.text for row in rows])
        self.assertNotIn('Carared', [row.text for row in rows])

    def test_user_deletes_grain_record(self):
        # Josh wants to contribute to the open source beer database.(Rave reviews from Kevin & John)
        # He navigates to the site (courtesy of Kevin)
        grain_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/grains')
        self.browser.get(grain_live_server_url)

        # He eagerly clicks the 'Add Grains' button

        self.browser.find_element_by_id("add_grain").click()

        self.browser.implicitly_wait(6)

        # He enters the information into the form and clicks submit.
        inputbox = self.browser.find_element_by_id('name')
        inputbox.send_keys('Crystal Malt')

        inputbox = self.browser.find_element_by_id('degrees_lovibond')
        inputbox.send_keys('19.00')

        inputbox = self.browser.find_element_by_id('specific_gravity')
        inputbox.send_keys('13.00')

        select = Select(self.browser.find_element_by_id('id_grain_type'))
        select.select_by_visible_text('Liquid Malt Extract')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Good standard malt for ales')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)

        # He sees the new grain record saved correctly
        self.find_text_in_table('Crystal Malt')

        # But there's a problem, he meant 'Chocolate Pale'! He
        # could change his entry, but he's in a hurry so he selects the delete link
        self.browser.find_element_by_link_text('Delete').click()
        self.browser.implicitly_wait(6)

        # The modal opens with the grain record details and asks him to confirm
        # that he wants to delete the record.
        submit_button = self.browser.find_element_by_id('delete').find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)

        # He confirms and the record is no longer visible on the grains main table.
        table = self.browser.find_element_by_id('list_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertNotIn('Crystal Malt', [row.text for row in rows])
