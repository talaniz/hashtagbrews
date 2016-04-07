from .base import FunctionalTest


class NewGrainVisitorTest(FunctionalTest):

    def test_user_can_navigate_to_grains_page_and_save_grains_record(self):
        # Kevin wants to contribute to the Open Source Homebrew Database
        # He navigates to the homepage and clicks the link to navigate
        # to the Open Source Homebrew database.
        self.browser.get(self.live_server_url)
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

        # He decides to try grains, clicks the Hops link and  is
        # redirected to the grains page.
        hops_link = self.browser.find_element_by_link_text('Grains')
        hops_link.click()

        page_heading = self.browser.find_element_by_tag_name('h1').text

        self.assertIn(page_heading, 'Grains')

        self.fail('Finish the test!')
