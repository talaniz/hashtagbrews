from selenium import webdriver
from selenium.webdriver.support.select import Select

from .base import FunctionalTest


class HopFormValidation(FunctionalTest):
    """
    User simulation entering blank or incorrect form data on hop forms
    """

    def test_addhops_blank_form_validation(self):
        """
        User performs the following tasks to submit blank hop form data:
                * User goes to the hops page
                * User submits new form with all blank fields
                * Check that 'addhops' form redirects to hops page with validation errors

                :return: pass or fail
        """

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

    def test_addhops_invalid_input_form_validation(self):
        """
        User performs the following tasks to input invalid data
                * User navigates directly to the hops page
                * User submits 'addhops' form with strings instead of numbers on min/max alpha acid
                * Check that the 'addhops' form redirects to the hops page with validation errors

                :return: pass or fail
        """

        # Ben wants to contribute to the Homebrew Database
        # He navigates to the hops page and selects 'Add Hops'
        hop_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/hops')
        self.browser.get(hop_live_server_url)

        self.browser.find_element_by_id("add_hops").click()

        self.browser.implicitly_wait(6)

        # He enters the information into the form and clicks submit.
        # He didn't realize that the alpha acid fields were for numbers
        # so he writes the out using letters instead.
        inputbox = self.browser.find_element_by_id('new_hops')
        inputbox.send_keys('Amarillo')

        inputbox = self.browser.find_element_by_id('min_alpha_acid')
        inputbox.send_keys('eight point three')

        inputbox = self.browser.find_element_by_id('max_alpha_acid')
        inputbox.send_keys('nine point three')

        select = Select(self.browser.find_element_by_id('id_country'))
        select.select_by_visible_text('United States')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Good over all aroma and bittering hops')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        self.browser.implicitly_wait(6)

        # Instead of seeing a new entry he sees the main hops page with
        # errors indicating that the fields are required should be a decimal number
        section_errors = self.browser.find_element_by_id('validation_errors')
        errors = section_errors.find_elements_by_tag_name('li')

        self.assertIn("Min alpha acid must be a decimal number", [error.text for error in errors])
        self.assertIn("Max alpha acid must be a decimal number", [error.text for error in errors])

        # TODO: invalid input for min/max alpha acid needs to specify the field name

    def test_update_hops_blank_input_validation(self):
        """
        User performs the following tasks to submit blank input on update form
                * User navigates to the hops page
                * User submits the 'addhops' form correctly
                * Check that form saved correctly
                * User clicks on hop name, clears all input fields, submits
                * Check redirect to hops page with validation errors

                :return: pass or fail
        """

        # Jim has decided to contribute to the open source homebrew database
        # He navigates to the hops page (Kevin showed him), and selects add hops
        hop_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/hops')
        self.browser.get(hop_live_server_url)

        self.browser.find_element_by_id("add_hops").click()

        self.browser.implicitly_wait(6)

        # He enters the information into the form and clicks submit.
        inputbox = self.browser.find_element_by_id('new_hops')
        inputbox.send_keys('Amarillo')

        inputbox = self.browser.find_element_by_id('min_alpha_acid')
        inputbox.send_keys('8.00')

        inputbox = self.browser.find_element_by_id('max_alpha_acid')
        inputbox.send_keys('11.00')

        select = Select(self.browser.find_element_by_id('id_country'))
        select.select_by_visible_text('United States')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Good over all aroma and bittering hops')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        # He closes out his browser, but then realizes that he's made a mistake.
        hops_page = self.browser.current_url
        self.browser.refresh()
        self.browser.quit()

        # He realizes the information he input was all wrong
        self.browser = webdriver.Firefox()
        self.browser.get(hops_page)

        self.browser.implicitly_wait(6)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(header_text, 'Hops')

        # He sees the link for the Amarillo hop record he just entered
        # and he clicks on it, a bootstrap modal form with the information
        # pops up
        self.browser.find_element_by_link_text('Amarillo').click()
        self.browser.implicitly_wait(6)

        # He can't remember the information, but he'll just clear out the fields
        # and enter the information later (Jim's a busy guy)
        inputbox = self.browser.find_element_by_id('update').find_element_by_id('new_hops')
        inputbox.clear()

        inputbox = self.browser.find_element_by_id('update').find_element_by_id('min_alpha_acid')
        inputbox.clear()

        inputbox = self.browser.find_element_by_id('update').find_element_by_id('max_alpha_acid')
        inputbox.clear()

        inputbox = self.browser.find_element_by_id('update').find_element_by_id('comments')
        inputbox.clear()

        submit_button = self.browser.find_element_by_id('update').find_element_by_id('submit')
        submit_button.click()

        # Instead of seeing his entry with blank forms, he is redirected
        # to the home page with errors displaying validation errors
        section_errors = self.browser.find_element_by_id('validation_errors')
        errors = section_errors.find_elements_by_tag_name('li')

        self.assertIn("A hop name is required", [error.text for error in errors])
        self.assertIn("You must enter a min alpha acid", [error.text for error in errors])
        self.assertIn("You must enter a max alpha acid", [error.text for error in errors])
        self.assertIn("You must enter a comment", [error.text for error in errors])

    def test_update_hops_invalid_input_validation(self):
        """
        User performs the following tasks to input invalid data in update form
                * User navigates directly to the hops page
                * User submits 'addhops' form correctly
                * Check that form data saved correctly
                * User clicks on hop name, changes min/max alpha acid to strings, submits
                * Check that 'addhops' form redirects to hops page with validation errors

                :return: pass or fail
        """

        # Jim has decided to contribute to the open source homebrew database
        # He navigates to the hops page (Kevin showed him), and selects add hops
        hop_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/hops')
        self.browser.get(hop_live_server_url)

        self.browser.find_element_by_id("add_hops").click()

        self.browser.implicitly_wait(6)

        # He enters the information into the form and clicks submit.
        inputbox = self.browser.find_element_by_id('new_hops')
        inputbox.send_keys('Amarillo')

        inputbox = self.browser.find_element_by_id('min_alpha_acid')
        inputbox.send_keys('8.00')

        inputbox = self.browser.find_element_by_id('max_alpha_acid')
        inputbox.send_keys('11.00')

        select = Select(self.browser.find_element_by_id('id_country'))
        select.select_by_visible_text('United States')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Good over all aroma and bittering hops')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        # He closes out his browser, but then realizes that he's made a mistake.
        hops_page = self.browser.current_url
        self.browser.refresh()
        self.browser.quit()

        # He realizes the information he input was all wrong
        self.browser = webdriver.Firefox()
        self.browser.get(hops_page)

        self.browser.implicitly_wait(6)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(header_text, 'Hops')

        # He sees the link for the Amarillo hop record he just entered
        # and he clicks on it, a bootstrap modal form with the information
        # pops up
        self.browser.find_element_by_link_text('Amarillo').click()
        self.browser.implicitly_wait(6)

        # He's distracted while he's fixing the information and accidentally spells out
        # the min and max alpha acid fields before submitting
        inputbox = self.browser.find_element_by_id('update').find_element_by_id('min_alpha_acid')
        inputbox.clear()

        inputbox.send_keys('one twenty')

        inputbox = self.browser.find_element_by_id('update').find_element_by_id('max_alpha_acid')
        inputbox.clear()

        inputbox.send_keys('twelve')

        submit_button = self.browser.find_element_by_id('update').find_element_by_id('submit')
        submit_button.click()

        # Instead of seeing his entry with blank forms, he is redirected
        # to the home page with errors displaying validation errors
        section_errors = self.browser.find_element_by_id('validation_errors')
        errors = section_errors.find_elements_by_tag_name('li')

        self.assertIn("Min alpha acid must be a decimal number", [error.text for error in errors])
        self.assertIn("Max alpha acid must be a decimal number", [error.text for error in errors])
