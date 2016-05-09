from app.tests.test_base import SeleniumTest

class AuthenticationTests(SeleniumTest):

    def test_can_login(self):
        # this test assumes init_db worked
        email = 'alpha1@email.com'
        password = 'password'
        self.login(email, password)

        e = self.client.find_element_by_css_selector('.alert')

        self.assertIn('Welcome', e.text)
        self.assertIn('dashboard', self.client.title.lower())

    def test_user_can_edit_an_address(self):
        # alpha1 needs to edit his current address
        self.login('alpha1@email.com', 'password')

        # on the dashboard there is a link to edit addresses
        link = self.client.find_element_by_link_text('Edit Mailing Address')
        link.click()

        # The current address is displayed here
        previous_address = self.client.find_element_by_css_selector('.address').text

        # there should be a link next to it that allows you to edit the address
        edit_link = self.client.find_element_by_css_selector('.address a')
        edit_link.click()

        # you are now at the edit address page
        street_address = self.client.find_element_by_id('street-address')
        city = self.client.find_element_by_id('city')
        state = self.client.find_element_by_id('state')
        postal_code = self.client.find_element_by_id('postal-code')
        country = self.client.find_element_by_id('country')

        # alpha1 edits his street_address
        street_address.clear()
        street_address.send_keys('444 new st')

        # alpha1 is content and now submits his changes
        self.client.find_element_by_xpath('//button[@type="submit"]').click()

        # he is redirected to the address page that shows the new changes
        new_address = self.client.find_element_by_css_selector('.address').text

        # if everything is good, the two should not be the same
        self.assertNotEqual(previous_address, new_address)

    def test_can_add_a_new_address_if_one_does_not_exist(self):
        # barbara registers
        self.register('barbara@email.com', 'barbara', 'password')

        self.go_to('dashboard')
        # she needs to add an address
        self.client.find_element_by_link_text('Edit Mailing Address').click()

        # There is a warning that states that there is currently no address on file
        warning = self.client.find_element_by_css_selector('h2')
        self.assertIn('No addresses found!', warning.text)

        # there is also a link to add an address
        link = warning.find_element_by_css_selector('a')

        # click it and get to the add address form
        link.click()
        heading = self.client.find_element_by_css_selector('h1')

        self.assertEqual('Add an Address', heading.text)

        # there are fields
        street_address = self.client.find_element_by_id('street-address')
        city = self.client.find_element_by_id('city')
        state = self.client.find_element_by_id('state')
        postal_code = self.client.find_element_by_id('postal-code')
        country = self.client.find_element_by_id('country')

        street_address.send_keys('123 apple st')
        city.send_keys('trees')
        state.send_keys('florida')
        postal_code.send_keys('44444-4444')
        country.send_keys('USA')

        self.client.find_element_by_xpath('//button[@type="submit"]').click()

        # she is taken to the address list page
        self.assertIn('Added new address', self.client.find_element_by_css_selector('.alert').text)
        self.assertIn('123 apple st', self.client.page_source)




