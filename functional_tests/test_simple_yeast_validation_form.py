import unittest

from selenium import webdriver
from selenium.webdriver.support.select import Select

from .base import FunctionalTest


class YeastFormValidation(FunctionalTest):
    """
    User simulation entering blank or incorrect form data on yeast forms
    """

    @unittest.skip('Form class pre-validates')
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
        self.auth_client(yeast_live_server_url)

        self.browser.find_element_by_id("add_yeasts").click()

        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

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
        self.auth_client(yeast_live_server_url)

        self.browser.find_element_by_id("add_yeasts").click()

        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

        # He enters the information into the form and clicks submit.
        # He didn't realize that some fields were for numbers
        # so he writes the out using letters instead.
        # He enters the information into the form and clicks submit

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

        inputbox = self.browser.find_element_by_id('name')
        inputbox.send_keys('American Ale 1056')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        self.browser.implicitly_wait(6)

        # Instead of seeing a new entry he sees the main hops page with
        # errors indicating that the fields are required should be a decimal number

        section_errors = self.browser.find_element_by_id('validation_errors')
        errors = section_errors.find_elements_by_tag_name('li')

        self.assertIn("Min temp must be a number", [error.text for error in errors])
        self.assertIn("Max temp must be a number", [error.text for error in errors])
        self.assertIn("Attenuation must be a number", [error.text for error in errors])

    def test_update_yeast_invalid_form_validation(self):
        """
        User performs the following tasks to input invalid data in update form
                * User navigates directly to the yeast page
                * User submits 'addyeasts' form correctly
                * Check that form data saved correctly
                * User clicks on yeast name, changes min/max temp & attenuation to
                strings, submits
                * Check that 'addyeasts' form redirects to yeast page with validation errors

                :return: pass or fail
        """

        # Jim has decided to contribute to the open source homebrew database
        # He navigates to the yeasts page (Kevin showed him), and selects add yeasts
        yeast_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/yeasts')
        self.auth_client(yeast_live_server_url)

        self.browser.find_element_by_id("add_yeasts").click()

        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

        # He enters the information into the form and clicks submit.

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
        inputbox.send_keys('25')

        select = Select(self.browser.find_element_by_id('flocculation'))
        select.select_by_visible_text('Medium')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Well balanced.')

        inputbox = self.browser.find_element_by_id('name')
        inputbox.send_keys('American Ale 1056')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        # He closes out his browser, but then realizes that he's made a mistake.
        yeast_page = self.browser.current_url
        self.browser.refresh()
        self.browser.quit()

        # He realizes the information he input was all wrong
        self.browser = webdriver.Firefox()
        self.auth_client(yeast_page)

        self.browser.implicitly_wait(6)

        yeasts_image = self.browser.find_elements_by_tag_name('img')
        yeasts_image_src = yeasts_image[1].get_attribute("src")

        self.assertIn('yeasts.jpg', yeasts_image_src)

        # He sees the link for the Amarillo hop record he just entered
        # and he clicks on it, a bootstrap modal form with the information
        # pops up
        self.browser.find_element_by_link_text('American Ale 1056').click()
        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

        # He's distracted while he's fixing the information and accidentally spells out
        # the min and max alpha acid fields before submitting
        inputbox = self.browser.find_element_by_id('update').find_element_by_id('min_temp')
        inputbox.clear()

        inputbox.send_keys('one twenty')

        inputbox = self.browser.find_element_by_id('update').find_element_by_id('max_temp')
        inputbox.clear()

        inputbox.send_keys('twelve')

        inputbox = self.browser.find_element_by_id('update').find_element_by_id('attenuation')
        inputbox.clear()

        inputbox.send_keys('thirteen')

        submit_button = self.browser.find_element_by_id('update').find_element_by_id('submit')
        submit_button.click()

        # Instead of seeing his entry with blank forms, he is redirected
        # to the home page with errors displaying validation errors
        section_errors = self.browser.find_element_by_id('validation_errors')
        errors = section_errors.find_elements_by_tag_name('li')

        self.assertIn("Min temp must be a number", [error.text for error in errors])
        self.assertIn("Min temp must be a number", [error.text for error in errors])
        self.assertIn("Attenuation must be a number", [error.text for error in errors])
