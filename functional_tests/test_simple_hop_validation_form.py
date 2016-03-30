from selenium.webdriver.support.select import Select

from .base import FunctionalTest


class HopFormValidation(FunctionalTest):

    def test_hops_blank_form_validation(self):
        # Ethan wants to contribute to the Homebrew Database
        # He navigates to the hops page and selects 'Add Hops'
        hop_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/hops')
        self.browser.get(hop_live_server_url)

        self.browser.find_element_by_id("add_hops").click()

        self.browser.implicitly_wait(6)

        # He suddenly realizes he doesn't know which hop record he would like to add.
        # So he figures he'll just add an empty record and edit it later
        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)
        # He hits enter on the blank form, but instead of seeing a new blank hop record,
        # he sees the main hops page with several errors indicating that the fields are required
        section_errors = self.browser.find_element_by_id('validation_errors')
        errors = section_errors.find_elements_by_tag_name('li')

        self.assertIn("A hop name is required", [error.text for error in errors])
        self.assertIn("You must enter a min alpha acid", [error.text for error in errors])
        self.assertIn("You must enter a max alpha acid", [error.text for error in errors])
        self.assertIn("You must enter a comment", [error.text for error in errors])

    def test_hops_invalid_input_form_validation(self):
        # Ethan wants to contribute to the Homebrew Database
        # He navigates to the hops page and selects 'Add Hops'
        hop_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/hops')
        self.browser.get(hop_live_server_url)

        self.browser.find_element_by_id("add_hops").click()

        self.browser.implicitly_wait(6)

        # He enters the information into the form and clicks submit.
        inputbox = self.browser.find_element_by_id('new_hops')
        inputbox.send_keys('Amarillo')

        inputbox = self.browser.find_element_by_id('min_alpha_acid')
        inputbox.send_keys('bad data')

        inputbox = self.browser.find_element_by_id('max_alpha_acid')
        inputbox.send_keys('more data')

        select = Select(self.browser.find_element_by_id('id_country'))
        select.select_by_visible_text('United States')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Good over all aroma and bittering hops')

        # He suddenly realizes he doesn't know which hop record he would like to add.
        # So he figures he'll just add an empty record and edit it later
        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        self.browser.implicitly_wait(6)
        # He hits enter on the blank form, but instead of seeing a new blank hop record,
        # he sees the main hops page with several errors indicating that the fields are required
        section_errors = self.browser.find_element_by_id('validation_errors')
        errors = section_errors.find_elements_by_tag_name('li')

        self.assertIn("This field requires a decimal number", [error.text for error in errors])
        self.assertIn("This field requires a decimal number", [error.text for error in errors])
