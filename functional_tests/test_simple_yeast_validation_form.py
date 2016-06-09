from selenium import webdriver
from selenium.webdriver.support.select import Select

from .base import FunctionalTest


class YeastFormValidation(FunctionalTest):
    """
    User simulation entering blank or incorrect form data on yeast forms
    """

    def test_add_yeast_blank_form_validation(self):
        """
        User performs the following tasks to submit blank yeast form data:
                * User goes to the yeasts page
                * User submits new form with all blank fields
                * Check that 'addyeasts' form redirects to yeasts page with validation errors

                :return: pass or fail
        """

        # Ethan wants to contribute to the Homebrew Database
        # He navigates to the yeasts page and selects 'Add Yeast'
        yeast_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/yeasts')
        self.browser.get(yeast_live_server_url)

        self.browser.find_element_by_id("add_yeasts").click()

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

        self.assertIn("A yeast name is required", [error.text for error in errors])
        self.assertIn("You must enter a min temp", [error.text for error in errors])
        self.assertIn("You must enter a max temp", [error.text for error in errors])
        self.assertIn("You must enter an attenuation", [error.text for error in errors])
        self.assertIn("You must enter a comment", [error.text for error in errors])
