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

    def test_add_yeast_invalid_input_form_validation(self):
        """
        User performs the following tasks to input invalid data
                * User navigates directly to the yeast page
                * User submits 'addyeasts' form with strings instead of numbers on min/max temp
                * Check that the 'addyeasts' form redirects to the hops page with validation errors

                :return: pass or fail
        """

        # Ben wants to contribute to the Homebrew Database
        # He navigates to the hops page and selects 'Add Hops'
        yeast_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/yeasts')
        self.browser.get(yeast_live_server_url)

        self.browser.find_element_by_id("add_yeasts").click()

        self.browser.implicitly_wait(6)

        # He enters the information into the form and clicks submit.
        # He didn't realize that the alpha acid fields were for numbers
        # so he writes the out using letters instead.
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
        inputbox.send_keys('sixty')

        inputbox = self.browser.find_element_by_id('max_temp')
        inputbox.send_keys('seventy two')

        inputbox = self.browser.find_element_by_id('attenuation')
        inputbox.send_keys('seventy five')

        select = Select(self.browser.find_element_by_id('flocculation'))
        select.select_by_visible_text('Medium')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Well balanced.')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        self.browser.implicitly_wait(6)

        # Instead of seeing a new entry he sees the main hops page with
        # errors indicating that the fields are required should be a decimal number

        section_errors = self.browser.find_element_by_id('validation_errors')
        errors = section_errors.find_elements_by_tag_name('li')

        self.assertIn("Min temp acid must be a number", [error.text for error in errors])
        self.assertIn("Max temp acid must be a number", [error.text for error in errors])