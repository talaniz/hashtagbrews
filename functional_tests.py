from selenium import webdriver
from selenium.webdriver.support.select import Select
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

        page_heading = self.browser.find_element_by_tag_name('h1').text

        self.assertIn(page_heading, 'Hops')

        # He finds the Add Hops button and clicks, a modal
        # form appears and he enters in a new hops name
        add_hops_link = self.browser.find_element_by_id("add_hops")
        add_hops_link.click()

        self.browser.implicitly_wait(10)

        # He enters the information into the form and clicks submit.
        inputbox = self.browser.find_element_by_id('new_hops')
        inputbox.send_keys('Amarillo')

        inputbox = self.browser.find_element_by_id('min_alpha_acid')
        inputbox.send_keys('8.00')

        inputbox = self.browser.find_element_by_id('max_alpha_acid')
        inputbox.send_keys('11.00')

        select = Select(self.browser.find_element_by_id('countries'))
        select.select_by_visible_text('USA')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Good over all aroma and bittering hops')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        # He can see the homepage with his hop record in the table
        table = self.browser.find_element_by_id('hops_list_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertIn('Amarillo', [row.text for row in rows])
        self.assertIn('8.00', [row.text for row in rows])
        self.assertIn('11.00', [row.text for row in rows])
        self.assertIn('USA', [row.text for row in rows])
        self.assertIn('Good over all aroma and bittering hops', [row.text for row in rows])

if __name__ == "__main__":
    unittest.main(warnings='ignore')