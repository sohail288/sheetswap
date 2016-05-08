from selenium.webdriver.support.select import Select
from app.tests.test_base import SeleniumTest
import time

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
        condition = Select(self.client.find_element_by_id('condition'))
        condition.select_by_visible_text('Torn pages, but all there')

        # and shes done
        self.client.find_element_by_xpath('//button[@type="submit"]').click()


        # she gets taken to the item page which lists the current details
        self.assertNotIn('update', self.client.current_url)

        # the changes made are reflected here
        heading = self.client.find_element_by_css_selector('#title')
        composer = self.client.find_element_by_css_selector('#composer')
        condition = self.client.find_element_by_css_selector('#condition')
        not_available_message = self.client.find_element_by_css_selector('.item-not-available')
        self.assertEqual('symphony #5', heading.text)
        self.assertEqual('beethoven', composer.text)
        self.assertEqual('Torn pages, but all there', condition.text)
        self.assertIn('this item is hidden from other users', not_available_message.text)

    def test_omega_can_access_her_items_from_her_dashboard(self):
        # omega signs in
        self.login('omega@email.com', 'password')

        # and there she sees her items
        self.client.find_element_by_css_selector('.items')
        items = self.client.find_elements_by_css_selector('.item-stub')

        # she can also edit them if she wants to
        edit_forms = self.client.find_elements_by_xpath('//div[@class="row items"]//form')

        self.assertEqual(len(items), len(edit_forms))

        # finally she can go directly to a page
        links = self.client.find_elements_by_css_selector('.item-stub  a')
        self.assertEqual(len(items), len(links))

        links[0].click()

        self.assertIn('items', self.client.current_url)
