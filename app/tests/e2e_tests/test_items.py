from selenium.webdriver.support.select import Select
from app.tests.test_base import SeleniumTest

class ItemTests(SeleniumTest):

    def test_can_create_item(self):
        self.fail("write this test")


    def test_omega_creates_an_item_and_then_modifies_it(self):

        # omega creates an item
        self.login('omega@email.com', 'password')
        self.create_item('symphony #5', 'beethoven', condition='Clean')

        # she is taken to the item page which shows the details of her item
        self.assertIn('items', self.client.current_url)
        heading = self.client.find_element_by_css_selector('#title')
        composer = self.client.find_element_by_css_selector('#composer')
        condition = self.client.find_element_by_css_selector('#condition')
        self.assertEqual('symphony #5', heading.text)
        self.assertEqual('beethoven', composer.text)
        self.assertEqual('Clean', condition.text)

        # she ends up wanting to modify some of the details about her item
        # there is an edit button somewhere on the page
        edit_button = self.client.find_element_by_css_selector('#edit-item')
        edit_button.click()

        # she makes the changes, the item isn't available right now, so she clicks that
        checkbox = self.client.find_element_by_xpath('//input[@type="checkbox"]')
        checkbox.click()

        # she messed up on the condition of the item so she changes that
        condition = Select(self.client.find_element_by_id('#condition'))
        condition.select_by_visible_text('Torn pages, but all there')

        # and shes down
        self.find_element_by_xpath('//button[type="submit"]').click()


        # she gets taken to the item page which lists the current details
        self.assertNotIn('update', self.client.current_url)

        # the changes made are reflected here
        heading = self.client.find_element_by_css_selector('#title')
        composer = self.client.find_element_by_css_selector('#composer')
        condition = self.client.find_element_by_css_selector('#condition')
        not_available_message = self.client.find_element_by_css_selector('.item-not-available')
        self.assertEqual('symphony #5', heading.text)
        self.assertEqual('beethoven', composer.text)
        self.assertEqual('Clean', condition.text)
        self.assertIn('this item is hidden from other users', not_available_message.text)

