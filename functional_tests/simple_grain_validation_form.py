from selenium import webdriver
from selenium.webdriver.support.select import Select

from .base import FunctionalTest


class GrainFormValidation(FunctionalTest):

    def test_addgrains_blank_form_validation(self):
        # Ethan wants to contribute to the Homebrew Database
        # He navigates to the hops page and selects 'Add Hops'
        grain_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/grains')
        self.browser.get(grain_live_server_url)

        self.browser.find_element_by_id("add_grain").click()

        self.browser.implicitly_wait(6)

        # He suddenly realizes he doesn't know which grain record he would like to add.
        # So he figures he'll just add an empty record and edit it later
        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)
        # He hits enter on the blank form, but instead of seeing a new blank grain record,
        # he sees the main hops page with several errors indicating that the fields are required
        section_errors = self.browser.find_element_by_id('validation_errors')
        errors = section_errors.find_elements_by_tag_name('li')

        self.assertIn("A grain name is required", [error.text for error in errors])
        self.assertIn("You must specify degrees lovibond", [error.text for error in errors])
        self.assertIn("You must enter a specific gravity", [error.text for error in errors])
        self.assertIn("You must leave a comment", [error.text for error in errors])