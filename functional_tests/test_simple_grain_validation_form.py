import unittest

from selenium import webdriver
from selenium.webdriver.support.select import Select

from .base import FunctionalTest


class GrainFormValidation(FunctionalTest):
    """
    User simulation entering blank or incorrect form data on grain forms
    """

    @unittest.skip('Form class pre-validates')
    def test_add_grains_blank_form_validation(self):
        """
        User performs the following tasks to submit blank grain form data:
                    * User goes to the grainss page
                    * User submits new form with all blank fields
                    * Check that 'addgrains' form redirects to grains page with validation errors

                    :return: pass or fail
        """

        # Ethan wants to contribute to the Homebrew Database
        # He navigates to the grains page and selects 'Add Grains'
        grain_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/grains')

        self.client.login(username='john75', password='sally75')
        cookie = self.client.cookies['sessionid']
        self.browser.get(grain_live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh() #need to update page for logged in user

        self.browser.find_element_by_id("add_grain").click()

        self.browser.implicitly_wait(6)

        # He suddenly realizes he doesn't know which grain record he would like to add.
        # So he figures he'll just add an empty record and edit it later
        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)
        # He hits enter on the blank form, but instead of seeing a new blank grain record,
        # he sees the main grains page with several errors indicating that the fields are required
        section_errors = self.browser.find_element_by_id('validation_errors')
        errors = section_errors.find_elements_by_tag_name('li')

        self.assertIn("A grain name is required", [error.text for error in errors])
        self.assertIn("You must specify degrees lovibond", [error.text for error in errors])
        self.assertIn("You must enter a specific gravity", [error.text for error in errors])
        self.assertIn("You must leave a comment", [error.text for error in errors])

    @unittest.skip('Form class pre-validates')
    def test_add_grains_invalid_input_form_validation(self):
        """
        User performs the following tasks to input invalid data
                * User navigates directly to the grains page
                * User submits 'addgrains' form with strings instead of numbers on degrees_lovibond & specific_gravity
                * Check that the 'addgrains' form redirects to the grain page with validation errors

                :return: pass or fail
        """

        # Ben wants to contribute to the Homebrew Database
        # He navigates to the grains page and selects 'Add Grains'
        grain_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/grains')

        self.client.login(username='john75', password='sally75')
        cookie = self.client.cookies['sessionid']
        self.browser.get(grain_live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh() #need to update page for logged in user

        self.browser.find_element_by_id("add_grain").click()

        self.browser.implicitly_wait(6)

        # He enters the information into the form and clicks submit.
        # He didn't realize that the alpha acid fields were for numbers
        # so he writes the out using letters instead.
        inputbox = self.browser.find_element_by_id('name')
        inputbox.send_keys('Amber Dry')

        inputbox = self.browser.find_element_by_id('degrees_lovibond')
        inputbox.send_keys('eight point three')

        inputbox = self.browser.find_element_by_id('specific_gravity')
        inputbox.send_keys('nine point three')

        select = Select(self.browser.find_element_by_id('id_grain_type'))
        select.select_by_visible_text('Liquid Malt Extract')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Malt extract for amber color')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        self.browser.implicitly_wait(6)

        # Instead of seeing a new entry he sees the main grains page with
        # errors indicating that the fields are required should be a decimal number
        section_errors = self.browser.find_element_by_id('validation_errors')
        errors = section_errors.find_elements_by_tag_name('li')

        self.assertIn("Degrees lovibond must be a decimal number", [error.text for error in errors])
        self.assertIn("Specific gravity must be a decimal number", [error.text for error in errors])

    @unittest.skip('Form class pre-validates')
    def test_update_grains_blank_form_validation(self):
        """
        User performs the following tasks to submit blank input on update form
                * User navigates to the grains page
                * User submits the 'addgrains' form correctly
                * Check that form saved correctly
                * User clicks on grain name, clears all input fields, submits
                * Check redirect to grains page with validation errors

                :return: pass or fail
        """

        # Jim has decided to contribute to the open source homebrew database
        # He navigates to the grains page (Kevin showed him), and selects add grain
        grain_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/grains')

        self.client.login(username='john75', password='sally75')
        cookie = self.client.cookies['sessionid']
        self.browser.get(grain_live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh() #need to update page for logged in user

        self.browser.find_element_by_id("add_grain").click()

        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

        # He enters the information into the form and clicks submit.
        inputbox = self.browser.find_element_by_id('name')
        inputbox.send_keys('Black Barley')

        inputbox = self.browser.find_element_by_id('degrees_lovibond')
        inputbox.send_keys('12.00')

        inputbox = self.browser.find_element_by_id('specific_gravity')
        inputbox.send_keys('125.00')

        select = Select(self.browser.find_element_by_id('id_grain_type'))
        select.select_by_visible_text('Liquid Malt Extract')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Imparts dryness. Unmalted; use in porters')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        # He closes out his browser, but then realizes that he's made a mistake.
        grains_page = self.browser.current_url
        self.browser.refresh()
        self.browser.quit()

        # He realizes the information he input was all wrong
        self.browser = webdriver.Firefox()

        self.client.login(username='john75', password='sally75')
        cookie = self.client.cookies['sessionid']
        self.browser.get(grains_page)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh() #need to update page for logged in user

        self.browser.implicitly_wait(6)

        grains_image = self.browser.find_elements_by_tag_name('img')
        grain_image_src = grains_image[1].get_attribute("src")

        self.assertIn('grains.jpg', grain_image_src)

        # He sees the link for the Black Barley grain record he just entered
        # and he clicks on it, a bootstrap modal form with the information
        # pops up
        self.browser.find_element_by_link_text('Black Barley').click()
        self.browser.implicitly_wait(6)

        # He can't remember the information, but he'll just clear out the fields
        # and enter the information later (Jim's a busy guy)
        inputbox = self.browser.find_element_by_id('update').find_element_by_id('name')
        inputbox.clear()

        inputbox = self.browser.find_element_by_id('update').find_element_by_id('degrees_lovibond')
        inputbox.clear()

        inputbox = self.browser.find_element_by_id('update').find_element_by_id('specific_gravity')
        inputbox.clear()

        inputbox = self.browser.find_element_by_id('update').find_element_by_id('comments')
        inputbox.clear()

        submit_button = self.browser.find_element_by_id('update').find_element_by_id('submit')
        submit_button.click()

        # Instead of seeing his entry with blank forms, he is redirected
        # to the home page with errors displaying validation errors
        section_errors = self.browser.find_element_by_id('validation_errors')
        errors = section_errors.find_elements_by_tag_name('li')

        self.assertIn("A grain name is required", [error.text for error in errors])
        self.assertIn("You must specify degrees lovibond", [error.text for error in errors])
        self.assertIn("You must enter a specific gravity", [error.text for error in errors])
        self.assertIn("You must leave a comment", [error.text for error in errors])

    def test_update_grains_invalid_form_validation(self):
        """
        User performs the following tasks to input invalid data in update form
                * User navigates directly to the grain page
                * User submits 'addgrains' form correctly
                * Check that form data saved correctly
                * User clicks on grain name, changes degrees_lovibond & specific_gravity to strings, submits
                * Check that 'addgrains' form redirects to grains page with validation errors

                :return: pass or fail
        """

        # Jim has decided to contribute to the open source homebrew database
        # He navigates to the grains page (Kevin showed him), and selects add grain
        grain_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/grains')

        self.client.login(username='john75', password='sally75')
        cookie = self.client.cookies['sessionid']
        self.browser.get(grain_live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh() #need to update page for logged in user


        self.browser.find_element_by_id("add_grain").click()

        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

        # He enters the information into the form and clicks submit.
        inputbox = self.browser.find_element_by_id('name')
        inputbox.send_keys('Black Barley')

        inputbox = self.browser.find_element_by_id('degrees_lovibond')
        inputbox.send_keys('12.00')

        inputbox = self.browser.find_element_by_id('specific_gravity')
        inputbox.send_keys('125.00')

        select = Select(self.browser.find_element_by_id('id_grain_type'))
        select.select_by_visible_text('Liquid Malt Extract')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Imparts dryness. Unmalted; use in porters')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        # He closes out his browser, but then realizes that he's made a mistake.
        grains_page = self.browser.current_url
        self.browser.refresh()
        self.browser.quit()

        # He realizes the specific gravity and degrees lovibond were wrong
        self.browser = webdriver.Firefox()

        self.client.login(username='john75', password='sally75')
        cookie = self.client.cookies['sessionid']
        self.browser.get(grains_page)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh() #need to update page for logged in user

        self.browser.implicitly_wait(6)

        grains_image = self.browser.find_elements_by_tag_name('img')
        grain_image_src = grains_image[1].get_attribute("src")

        self.assertIn('grains.jpg', grain_image_src)

        # He sees the link for the Black Barley grain record he just entered
        # and he clicks on it, a bootstrap modal form with the information
        # pops up
        self.browser.find_element_by_link_text('Black Barley').click()
        self.browser.implicitly_wait(6)

        # While he's correcting the information, he gets distracted and accidentally
        # spells out the fields instead of using numbers
        inputbox = self.browser.find_element_by_id('update').find_element_by_id('degrees_lovibond')
        inputbox.clear()

        inputbox.send_keys('twelve')

        inputbox = self.browser.find_element_by_id('update').find_element_by_id('specific_gravity')
        inputbox.clear()

        inputbox.send_keys('one twenty')

        submit_button = self.browser.find_element_by_id('update').find_element_by_id('submit')
        submit_button.click()

        # Instead of seeing his entry with blank forms, he is redirected
        # to the home page with errors displaying validation errors
        section_errors = self.browser.find_element_by_id('validation_errors')
        errors = section_errors.find_elements_by_tag_name('li')

        self.assertIn("Degrees lovibond must be a decimal number", [error.text for error in errors])
        self.assertIn("Specific gravity must be a decimal number", [error.text for error in errors])
