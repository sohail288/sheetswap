from app.tests.test_base import SeleniumTest

class AuthenticationTests(SeleniumTest):

    def test_can_login(self):
        # this test assumes init_db worked
        email = 'alpha1@email.com'
        password = 'password'
        self.login(email, password)

        e = self.client.find_element_by_css_selector('.alert')

        self.assertIn('Welcome', e.text)
