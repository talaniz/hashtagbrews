from selenium import webdriver
from selenium.webdriver.support.select import Select

from .base import FunctionalTest


class SimpleLoginTest(FunctionalTest):

    def test_user_can_login(self):
        """
        Test to verify that user can log into the site.

        User performs the following steps to complete the test:
                * Click login link
                * Enter username and password
                * Navigate to the hops page and find the add hops button
        :return:
        """

        # Josh wants to visit the homebrew materials database to
        # contribute. He opens his web browser and navigates to the site.
        self.browser.get(self.live_server_url)
        self.browser.implicitly_wait(5)

        # He looks for the login link and clicks it
        login_link = self.browser.find_element_by_link_text('Login')
        login_link.click()
        self.browser.implicitly_wait(5)

        grains_image = self.browser.find_elements_by_tag_name('img')
        grain_image_src = grains_image[1].get_attribute("src")

        self.assertIn('login.jpg', grain_image_src)

        # He enters his username and password and clicks login
        username_box = self.browser.find_element_by_id('id_username')
        username_box.send_keys('john75')

        password_box = self.browser.find_element_by_id('id_password')
        password_box.send_keys('sally75')

        login_button = self.browser.find_element_by_id('submit')
        login_button.click()
        self.browser.implicitly_wait(5)

        # The site redirects him to the homebrew database page
        page_heading = self.browser.find_element_by_tag_name('h1')

        self.assertIn("Homebrew Materials Database", page_heading.text)

        # He navigates to the hops page and adds a record and clicks submit
        hops_link = self.browser.find_element_by_link_text('Hops')

        hops_link.click()
        self.browser.implicitly_wait(5)

        hops_image = self.browser.find_elements_by_tag_name('img')
        hops_image_src = hops_image[1].get_attribute("src")

        self.assertIn('hops.jpg', hops_image_src)

        self.browser.find_element_by_id("add_hops").click()

        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

        # He enters the information into the form and clicks submit.
        inputbox = self.browser.find_element_by_id('new_hops')
        inputbox.send_keys('Amarillo')

        inputbox = self.browser.find_element_by_id('min_alpha_acid')
        inputbox.send_keys('8.52')

        inputbox = self.browser.find_element_by_id('max_alpha_acid')
        inputbox.send_keys('11.33')

        select = Select(self.browser.find_element_by_id('id_country'))
        select.select_by_visible_text('United States')

        inputbox = self.browser.find_element_by_id('comments')
        inputbox.send_keys('Good over all aroma and bittering hops')

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(6)
        self.browser.switch_to.active_element

        self.find_text_in_table('Amarillo')
        self.find_text_in_table('8.52')
        self.find_text_in_table('11.33')
        self.find_text_in_table('USA')
        self.find_text_in_table('Good over all aroma and bittering hops')

        # After reviewing the record, he's satisfied and clicks logout
        logout_link = self.browser.find_element_by_link_text('Logout')
        logout_link.click()
        self.browser.implicitly_wait(5)

        # He's then redirected to the login page and closes out his web browser
        page_heading = self.browser.find_element_by_link_text('Login')

        self.assertIn("Login", page_heading.text)
