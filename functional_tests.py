from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    '''
    Test to check new visitor functionality
    '''

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_home_page_redirects_to_beer_database(self):

        # Kevin wants to contribute to the Open Source Homebrew Database
        # He navigates to the homepage and clicks the link to navigate
        # to the Open Source Homebrew database.
        self.browser.get('http://localhost:8000')

        beerdb_link = self.browser.find_element_by_id('beerdb').text

        self.assertEqual(beerdb_link, 'Open Source Beer Database')

        # He is redirected to the hops page and sees a button
        # 'Add a hop'. He clicks the button and a form appears.
        hops_link = self.browser.find_element_by_link_text('Hops')
        hops_link.click()

        self.browser.implicitly_wait(3)

    def test_can_add_hop_record_and_save(self):

        # Finds the Add Hops button and clicks, then switches to new modal
        # to submit form
        self.browser.find_element_by_class("btn btn-primary")
        self.browser.switchTo().frame("AddHops")

        form_header = self.browser.find_element_by_tag_name('h3').text

        self.assertEqual(form_header, 'New Hops')
        # He enters the information into the form and hits submit.
        # He can see the homepage with his hop record in the table
        self.fail("Finish the test")

        # TODO add the rest of the form submission
        '''
        inputbox = self.browser.find_element_by_id('hop_name')
        inputbox.send_keys('Amarillo')
        '''
