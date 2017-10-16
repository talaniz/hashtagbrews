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

        hops_image = self.browser.find_elements_by_tag_name('img')
        hops_image_src = hops_image[1].get_attribute("src")

        self.assertIn('hops.jpg', hops_image_src)

        # He finds the Add Hops button and clicks, a modal
        # form appears and he enters in a new hops name
        self.browser.find_element_by_id("add_hops").click()

        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

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
        self.browser.switch_to.active_element

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
        self.browser.switch_to.active_element

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
        # self.browser.implicitly_wait(6)

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


class SimpleGrainTest(FunctionalTest):

    def test_simple_grain_search(self):
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
        self.browser.switch_to.active_element

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

        # He adds another record that he can remember
        self.browser.find_element_by_id("add_grain").click()
        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

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

        # He adds a third record--
        self.browser.find_element_by_id("add_grain").click()
        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

        inputbox = self.browser.find_element_by_id('name')
        inputbox.send_keys('Black Barley')

        inputbox = self.browser.find_element_by_id('degrees_lovibond')
        inputbox.send_keys('2.3')

        inputbox = self.browser.find_element_by_id('specific_gravity')
        inputbox.send_keys('3.25')

        select = Select(self.browser.find_element_by_id('id_grain_type'))
        select.select_by_visible_text('Grain')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Dark, biscuit flavor')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

        # He sees the search bar and enters the name of his hops to see if it will
        # appear and clicks submit
        inputbox = self.browser.find_element_by_id('query')
        inputbox.send_keys('Black Barley')

        submit_button = self.browser.find_elements_by_id('submit')[3]
        submit_button.click()
        self.browser.implicitly_wait(6)

        # The page redirects and he sees the table wih the name of the hops
        # He can see the homepage only with hop records that match his search
        self.find_text_in_table('Black Barley')
        self.find_text_in_table('2.3')
        self.find_text_in_table('3.25')
        self.find_text_in_table('GRN')
        self.find_text_in_table('Dark, biscuit flavor')

        self.find_text_not_in_table('Crystal Malt')
        self.find_text_not_in_table('19.00')
        self.find_text_not_in_table('13.00')
        self.find_text_not_in_table('Liquid Malt Extract')
        self.find_text_not_in_table('Good standard malt for ales')

        # Satisfied, he closes his browser and brews some beer


class SimpleYeastSearchTest(FunctionalTest):

    def test_simple_yeast_search(self):
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
        grains_link = self.browser.find_element_by_link_text('Yeasts')
        grains_link.click()

        page_heading = self.browser.find_element_by_tag_name('h1').text

        self.assertIn(page_heading, 'Yeasts')

        # He finds the Add Grain button and clicks, a modal
        # form appears and he enters in a new grain name
        self.browser.find_element_by_id("add_yeasts").click()

        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

        # He enters the information into the form and clicks submit
        inputbox = self.browser.find_element_by_id('name')
        inputbox.send_keys('American Ale II 1272')

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
        select.select_by_visible_text('Low')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Well balanced.')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)

        # He adds another record that he can remember
        self.browser.find_element_by_id("add_yeasts").click()
        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

        # He enters the information into the form and clicks submit
        inputbox = self.browser.find_element_by_id('name')
        inputbox.send_keys('American Ale 1056')

        select = Select(self.browser.find_element_by_id('lab'))
        select.select_by_visible_text('Brewtek')

        select = Select(self.browser.find_element_by_id('yeast_type'))
        select.select_by_visible_text('Saison')

        select = Select(self.browser.find_element_by_id('yeast_form'))
        select.select_by_visible_text('Liquid')

        inputbox = self.browser.find_element_by_id('min_temp')
        inputbox.send_keys('61')

        inputbox = self.browser.find_element_by_id('max_temp')
        inputbox.send_keys('72')

        inputbox = self.browser.find_element_by_id('attenuation')
        inputbox.send_keys('76')

        select = Select(self.browser.find_element_by_id('flocculation'))
        select.select_by_visible_text('Medium')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Well balanced.')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)

        # He adds a third record--
        self.browser.find_element_by_id("add_yeasts").click()
        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

        inputbox = self.browser.find_element_by_id('name')
        inputbox.send_keys('Ringwood Ale 1187')

        select = Select(self.browser.find_element_by_id('lab'))
        select.select_by_visible_text('Wylabs')

        select = Select(self.browser.find_element_by_id('yeast_type'))
        select.select_by_visible_text('Wheat')

        select = Select(self.browser.find_element_by_id('yeast_form'))
        select.select_by_visible_text('Dry')

        inputbox = self.browser.find_element_by_id('min_temp')
        inputbox.send_keys('64')

        inputbox = self.browser.find_element_by_id('max_temp')
        inputbox.send_keys('74')

        inputbox = self.browser.find_element_by_id('attenuation')
        inputbox.send_keys('70')

        select = Select(self.browser.find_element_by_id('flocculation'))
        select.select_by_visible_text('High')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('A malty, complex profile that clears well.')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

        # He sees the search bar and enters the name of his hops to see if it will
        # appear and clicks submit
        inputbox = self.browser.find_element_by_id('query')
        inputbox.send_keys('American')

        submit_button = self.browser.find_elements_by_id('submit')[3]
        submit_button.click()
        self.browser.implicitly_wait(6)

        # The page redirects and he sees the table wih the name of the hops
        # He can see the homepage only with hop records that match his search
        self.find_text_in_table('American Ale II 1272')
        self.find_text_in_table('Wyeast')
        self.find_text_in_table('Ale')
        self.find_text_in_table('Liquid')
        self.find_text_in_table('60')
        self.find_text_in_table('72')
        self.find_text_in_table('75')
        self.find_text_in_table('Medium')
        self.find_text_in_table('Well balanced.')

        self.find_text_in_table('American Ale 1056')
        self.find_text_in_table('Wyeast')
        self.find_text_in_table('Ale')
        self.find_text_in_table('Liquid')
        self.find_text_in_table('61')
        self.find_text_in_table('72')
        self.find_text_in_table('76')
        self.find_text_in_table('High')
        self.find_text_in_table('A malty, complex profile that clears well.')

        self.find_text_not_in_table('Ringwood Ale 1187')
        self.find_text_not_in_table('Wylabs')
        self.find_text_not_in_table('Wheat')
        self.find_text_not_in_table('Dry')
        self.find_text_not_in_table('64')
        self.find_text_not_in_table('74')
        self.find_text_not_in_table('70')
        self.find_text_not_in_table('High')
        self.find_text_not_in_table('A malty, complex profile that clears well.')

        # Satisfied, he closes his browser and brews some beer
