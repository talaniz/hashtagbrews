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


class SimpleRegistrationTest(FunctionalTest):

    def test_user_can_register(self):
        """The user should be logged in after registration."""

        # Charlie wants to visit the homebrew materials database to
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

        # He realizes that he doesn't have a user name and password
        # so he clicks register and is redirected to a registration form.
        reg_link = self.browser.find_element_by_link_text('Register')
        reg_link.click()
        self.browser.implicitly_wait(5)

        # He fills in the form to register and clicks submit
        password_box = self.browser.find_element_by_id('id_username')
        password_box.send_keys('ckelly')

        email_box = self.browser.find_element_by_id('id_email')
        email_box.send_keys('ckelly@kellyandasscts.com')

        password1_box = self.browser.find_element_by_id('id_password1')
        password1_box.send_keys('birdlaws')

        password2_box = self.browser.find_element_by_id('id_password2')
        password2_box.send_keys('birdlaws')

        login_button = self.browser.find_element_by_id('submit')
        login_button.click()
        self.browser.implicitly_wait(5)

        # The site redirects him to the homebrew database page
        page_heading = self.browser.find_element_by_tag_name('h1')

        self.assertIn("Homebrew Materials Database", page_heading.text)

        # He sees his username in the top right corner indicating that he's
        # logged in.
        user_profile = self.browser.find_element_by_link_text('ckelly')
        self.assertEqual(user_profile.text, 'ckelly')

        # He clicks the logout link
        logout_link = self.browser.find_element_by_link_text('Logout')
        logout_link.click()
        self.browser.implicitly_wait(5)

        # He's then redirected to the login page. To be sure he's remembered
        # his password, he clicks login one more time and logs in.
        page_heading = self.browser.find_element_by_link_text('Login')
        page_heading.click()
        self.browser.implicitly_wait(5)
        #self.assertIn("Login", page_heading.text)
        # He enters his username and password and clicks login
        username_box = self.browser.find_element_by_id('id_username')
        username_box.send_keys('ckelly')

        password_box = self.browser.find_element_by_id('id_password')
        password_box.send_keys('birdlaws')

        login_button = self.browser.find_element_by_id('submit')
        login_button.click()
        self.browser.implicitly_wait(5)

        # The site redirects him to the homebrew database page
        page_heading = self.browser.find_element_by_tag_name('h1')

        self.assertIn("Homebrew Materials Database", page_heading.text)

        # He sees his username in the top right corner indicating that he's
        # logged in.
        user_profile = self.browser.find_element_by_link_text('ckelly')
        self.assertEqual(user_profile.text, 'ckelly')

        # Satisfied, he clicks the logout link and closes his computer
        logout_link = self.browser.find_element_by_link_text('Logout')
        logout_link.click()
        self.browser.implicitly_wait(5)
