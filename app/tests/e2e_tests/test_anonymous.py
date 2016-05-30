from selenium.common.exceptions import NoSuchElementException
from app.tests.test_base import SeleniumTest
import random


class AnonymousTests(SeleniumTest):

    def test_anonymous_users_can_browse_sheet_music(self):
        # a pontential user has heard about SheetSwap
        # she goes over to the website
        self.client.get("{}/".format(self.server_url))

        # she sees that there is a login button
        login_button = self.client.find_element_by_link_text('Login')

        # she clicks on the login button to see what its about
        login_button.click()

        # she is brought to the login page that has a form to input an email and password
        try:
            email_input = self.client.find_element_by_xpath('//input[@id="email"]')
        except NoSuchElementException:
            self.fail("She couldn't find the damn login input")

        # great so, she doesn't want to login or do anything yet she just wants to see the
        # available sheetmusic
        # she sees that there is a sheets button
        sheets_button = self.client.find_element_by_link_text('Sheets')

        # she clicks on it
        sheets_button.click()

        # she is brought to the sheet music page
        # she sees that there are a lot of sheets to choose from!
        sheets = self.client.find_elements_by_css_selector('.sheet-music-stub')


        # she picks a sheet
        chosen_sheet = random.choice(sheets)

        # she found this one because the title got her interested
        title = chosen_sheet.find_element_by_css_selector('.panel-heading').text

        # she clicks on the link
        chosen_sheet.find_element_by_tag_name('a').click()

        # she is now taken to a page that contains all the items available for that sheetmusic
        item_page_title = self.client.find_element_by_tag_name('h1').text

        # the page title has her reassured that shes on the correct page
        self.assertIn(title, item_page_title)

        # this page has quite a few sheets available
        try:
            self.client.find_elements_by_css_selector('.item_stub')
        except NoSuchElementException:
            self.fail("failed to find any items")

        # normally you can trade items, but our new user cannot, she should not see a trade link
        with self.assertRaises(NoSuchElementException):
            self.client.find_element_by_tag_name('form')

        # satisified she closes her browser


    def test_anonymous_users_can_register_if_they_want_to(self):
        # the potential user is back and wants to register
        self.client.get("{}/".format(self.server_url))
        login_button = self.client.find_element_by_link_text('Login')
        login_button.click()

        # she sees that there is a link to register
        register_link = self.client.find_element_by_link_text('Register')

        # she clicks it and goes to the register page
        register_link.click()

        # here she is faced with a simple registration form
        # she fills it out following all the instructions
        email = self.client.find_element_by_id('email')
        username = self.client.find_element_by_id('username')
        password = self.client.find_element_by_id('password')
        check_password = self.client.find_element_by_id('check_password')

        email.send_keys('barbara@email.com')
        username.send_keys('barbara')
        password.send_keys('password')
        check_password.send_keys('password')

        # she sees the submit button
        submit = self.client.find_element_by_xpath('//button[@type="submit"]')

        # she clicks it
        submit.click()

        # she is taken to the main page
        self.assertEqual(self.client.current_url, "{}/".format(self.server_url))

        # where she sees that there is an alert
        alert = self.client.find_element_by_css_selector('.alert')

        # that says thanks for registering
        self.assertIn('Thanks for registering', alert.text)


    def test_new_users_are_alerted_if_they_try_to_create_an_already_existing_account(self):
        username = 'testuser'
        email = username + '@email.com'
        password = '1234'

        self.register(email, username, password)

        # they try it again
        self.go_to('auth/logout')

        self.register(email, username, password)

        alert = self.client.find_element_by_css_selector('.alert')

        self.assertIn('That email or username already exists!', alert.text)
