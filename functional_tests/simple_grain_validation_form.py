from selenium import webdriver
from selenium.webdriver.support.select import Select

from .base import FunctionalTest


class GrainFormValidation(FunctionalTest):

    def test_addgrains_blank_form_validation(self):
        # Ethan wants to contribute to the Homebrew Database
        # He navigates to the grains page and selects 'Add Grains'
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
        # he sees the main grains page with several errors indicating that the fields are required
        section_errors = self.browser.find_element_by_id('validation_errors')
        errors = section_errors.find_elements_by_tag_name('li')

        self.assertIn("A grain name is required", [error.text for error in errors])
        self.assertIn("You must specify degrees lovibond", [error.text for error in errors])
        self.assertIn("You must enter a specific gravity", [error.text for error in errors])
        self.assertIn("You must leave a comment", [error.text for error in errors])

    def test_addgrains_invalid_input_form_validation(self):
        # Ben wants to contribute to the Homebrew Database
        # He navigates to the grains page and selects 'Add Grains'
        grain_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/grains')
        self.browser.get(grain_live_server_url)

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

    def test_update_grains_blank_form_validation(self):
        # Jim has decided to contribute to the open source homebrew database
        # He navigates to the grains page (Kevin showed him), and selects add grain
        grain_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/grains')
        self.browser.get(grain_live_server_url)

        self.browser.find_element_by_id("add_grain").click()

        self.browser.implicitly_wait(6)

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
        self.browser.get(grains_page)

        self.browser.implicitly_wait(6)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(header_text, 'Grains')

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
        self.assertIn("You must enter a comment", [error.text for error in errors])