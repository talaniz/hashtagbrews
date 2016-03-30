from .base import FunctionalTest


class HopFormValidation(FunctionalTest):

    def test_hops_empty_form_validation(self):
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