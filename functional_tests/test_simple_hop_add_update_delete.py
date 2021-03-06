from selenium import webdriver
from selenium.webdriver.support.select import Select

from .base import FunctionalTest


class NewHopsVisitorTest(FunctionalTest):
    """
    Simulation of a first time user adding yeast records

    * Note: View[Model]Visitor tests could use a helper function to navigate through the first 2 pages at this point
    """

    def test_user_can_navigate_to_hops_page_and_save_hops_record(self):
        """
        User performs the following tasks to add hop record:
                * Navigate to site index
                * Navigate to homebrew database page
                * Select 'Hops' & redirect to hops main page
                * Click on modal 'Add Hops', fill in form & submit
                * Check for submitted record on hops page
                * Quite browser, reopen hops main page and re-check for record

                :return: pass or fail
        """

        # Kevin wants to contribute to the Open Source Homebrew Database
        # He navigates to the homepage and clicks the link to navigate
        # to the Open Source Homebrew database.
        self.client.login(username='john75', password='sally75')
        cookie = self.client.cookies['sessionid']
        self.browser.get(self.live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh() #need to update page for logged in user
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

        hops_image = self.browser.find_elements_by_tag_name('img')
        hops_image_src = hops_image[1].get_attribute("src")

        self.assertIn('hops.jpg', hops_image_src)

        # He finds the Add Hops button and clicks, a modal
        # form appears and he enters in a new hops name
        self.browser.find_element_by_id("add_hops").click()

        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

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
        self.browser.implicitly_wait(6)

        # He can see the homepage with his hop record in the table
        self.find_text_in_table('Amarillo')
        self.find_text_in_table('8.0')
        self.find_text_in_table('11.0')
        self.find_text_in_table('USA')
        self.find_text_in_table('Good over all aroma and bittering hops')

        # Satisfied, he closes his browser and brews some beer
        hops_page = self.browser.current_url
        self.browser.refresh()
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Kevin wonders if the site really saved his record.
        # He opens up the browser to the hops main page and checks
        # to make sure the information he entered is still here
        self.browser.get(hops_page)

        self.find_text_in_table('Amarillo')
        self.find_text_in_table('8.0')
        self.find_text_in_table('11.0')
        self.find_text_in_table('USA')
        self.find_text_in_table('Good over all aroma and bittering hops')

        # Satisfied once again, he returns to his boil.

    def test_user_can_update_hop_record(self):
        """
        User performs the following tasks to update hop record:
                * Navigate to hops
                * Select 'Hops' & redirect to hops main page
                * Click on modal 'Add Hops', fill in form & submit
                * Check for submitted record on hops page
                * Click on hop name, change field name in modal, save
                * Check hops page to make sure record was successfully updated

                :return: pass or fail
        """

        # John has decided to contribute to the open source homebrew database
        # He navigates to the hops page (Kevin showed him), and selects add hops
        hop_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/hops')

        self.client.login(username='john75', password='sally75')
        cookie = self.client.cookies['sessionid']
        self.browser.get(hop_live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh() #need to update page for logged in user
        self.browser.implicitly_wait(5)

        self.browser.find_element_by_id("add_hops").click()

        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

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

        # The hop name wasn't 'Amarillo' it was 'Chinook'. He decides to go back and update the record
        self.browser = webdriver.Firefox()

        self.client.login(username='john75', password='sally75')
        cookie = self.client.cookies['sessionid']
        self.browser.get(hops_page)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh() #need to update page for logged in user

        self.browser.implicitly_wait(6)

        hops_image = self.browser.find_elements_by_tag_name('img')
        hops_image_src = hops_image[1].get_attribute("src")

        self.assertIn('hops.jpg', hops_image_src)

        # He sees the link for the Amarillo hop record he just entered
        # and he clicks on it, a bootstrap modal form with the information
        # pops up
        self.browser.find_element_by_link_text('Amarillo').click()
        self.browser.implicitly_wait(6)

        # He changes the hop name from Amarillo to Chinook and clicks submit.
        # He's redirected back to the hops list page and can see the change updated
        # in the table
        inputbox = self.browser.find_element_by_id('update').find_element_by_id('new_hops')

        inputbox.clear()
        inputbox.send_keys('Chinook')

        submit_button = self.browser.find_element_by_id('update').find_element_by_id('submit')
        submit_button.click()

        table = self.browser.find_element_by_id('list_table')
        rows = table.find_elements_by_tag_name('td')

        self.assertIn('Chinook', [row.text for row in rows])
        self.assertNotIn('Amarillo', [row.text for row in rows])

    def test_user_deletes_hop_record(self):
        """
        User performs the following tasks to delete hop record:
                * Navigate to hops
                * Select 'Hops' & redirect to hops main page
                * Click on modal 'Add Hops', fill in form & submit
                * Check for submitted record on hops page
                * Click on 'Delete' link, confirm delete
                * Check hops page to make sure record was successfully deleted

                :return: pass or fail
        """

        # Josh wants to contribute to the open source beer database.(Rave reviews from Kevin & John)
        # He navigates to the site (courtesy of Kevin)
        hop_live_server_url = '{0}{1}'.format(self.live_server_url, '/beerdb/hops')

        self.client.login(username='john75', password='sally75')
        cookie = self.client.cookies['sessionid']
        self.browser.get(hop_live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh() #need to update page for logged in user

        # He eagerly clicks the 'Add Hops' button

        self.browser.find_element_by_id("add_hops").click()

        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

        # He enters the information into the form and clicks submit.
        inputbox = self.browser.find_element_by_id('new_hops')
        inputbox.send_keys('Northern')

        inputbox = self.browser.find_element_by_id('min_alpha_acid')
        inputbox.send_keys('9.00')

        inputbox = self.browser.find_element_by_id('max_alpha_acid')
        inputbox.send_keys('13.00')

        select = Select(self.browser.find_element_by_id('id_country'))
        select.select_by_visible_text('Australia')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Good for bittering, bad for aroma')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)

        # He sees the new hop record saved correctly
        self.find_text_in_table('Northern')

        # But there's a problem, he meant 'Chinook'! He
        # could change his entry, but he's in a hurry so he selects the delete link
        self.browser.find_element_by_link_text('Delete').click()
        self.browser.implicitly_wait(6)

        # The modal opens with the hop record details and asks him to confirm
        # that he wants to delete the record.
        submit_button = self.browser.find_element_by_id('delete').find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)

        # He confirms and the record is no longer visible on the hops main table.
        table = self.browser.find_element_by_id('list_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertNotIn('Northern', [row.text for row in rows])


        # TODO: write test for unique hop records
