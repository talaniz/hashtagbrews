from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    '''
    Test to check new visitor functionality
    '''

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.set_window_size(1750, 1000)

    def tearDown(self):
        self.browser.quit()

    def test_user_can_navigate_to_hops_page_and_save_hops_record(self):

        # Kevin wants to contribute to the Open Source Homebrew Database
        # He navigates to the homepage and clicks the link to navigate
        # to the Open Source Homebrew database.
        self.browser.get('http://localhost:8000')
        self.browser.implicitly_wait(5)

        beerdb_link = self.browser.find_element_by_id('beerdb').text

        self.assertEqual(beerdb_link, 'Homebrew Database')

        # He's redirected to the Homebrew Materials Database and
        # sees this listed in the title and the body of the page
        beerdb_link = self.browser.find_element_by_id('beerdb')

        beerdb_link.click()

        page_heading = self.browser.find_element_by_tag_name('h1')

        self.assertIn("Homebrew Materials Database", page_heading.text)

        # Kevin is presented with 3 categories to choose from: Hops, Grains and Yeasts
        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertIn('Hops', page_text)
        self.assertIn('Grains', page_text)
        self.assertIn('Yeasts', page_text)

        # He decides to try hops, clicks the Hops link and  is
        # redirected to the hops page.
        hops_link = self.browser.find_element_by_link_text('Hops')
        hops_link.click()

        self.browser.implicitly_wait(5)

        page_heading = self.browser.find_element_by_tag_name('h1').text

        self.assertIn(page_heading, 'Hops')

        # He finds the Add Hops button and clicks, then switches to new modal
        # to submit form
        self.browser.find_element_by_id("add_hops")
        self.browser.switch_to.active_element()

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
if __name__ == "__main__":
    unittest.main(warnings='ignore')