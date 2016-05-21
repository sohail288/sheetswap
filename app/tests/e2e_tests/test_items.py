from urllib.request import urlretrieve
from os.path import exists
import os
from selenium.webdriver.support.select import Select
from app.tests.test_base import SeleniumTest
import time


def get_a_sample_image_file():
    filename = 'test_image.jpg'
    wd = os.getcwd()
    filename = os.path.join(wd, filename)
    if not exists(filename):
        urlretrieve('https://upload.wikimedia.org/wikipedia/commons/b/b2/B8-2_Broken_Metronome.jpg', filename)
    return filename


class ItemTests(SeleniumTest):

    def test_can_create_item(self):
        filename = get_a_sample_image_file()
        title = 'Sonata for Piano'
        composer = 'Beethoven'
        instrumentation = 'piano'
        genre = 'classical'
        time_signature = '3/4'
        cover = filename
        condition = 'Oldish'

        # omega is at it again
        self.login('omega@email.com', 'password')

        # In her dashboard, there is an option to add a new item
        create_item_link = self.client.find_element_by_css_selector('#create-item-link')

        create_item_link.click()

        # she is adding a new sheet to the database
        self.client.find_element_by_id('title').send_keys(title)
        self.client.find_element_by_id('composer').send_keys(composer)
        self.client.find_element_by_id('instrumentation').send_keys(instrumentation)
        self.client.find_element_by_id('genre').send_keys(genre)
        self.client.find_element_by_id('time_signature').send_keys(time_signature)
        self.client.find_element_by_id('cover').send_keys(cover)
        self.client.find_element_by_xpath('//button[@type="submit"]').click()

        # now it says that her sheetmusic has been made
        alert = self.client.find_element_by_css_selector('.alert')
        self.assertIn('{} has been added'.format(title), alert.text)

        # she needs to enter the details for her item
        self.client.find_element_by_id('description').send_keys('good stuff here')
        dd = Select(self.client.find_element_by_id('condition'))
        dd.select_by_visible_text(condition)
        self.client.find_element_by_xpath('//button[@type="submit"]').click()

        alert = self.client.find_element_by_css_selector('.alert')
        self.assertIn('You just made a new item!', alert.text)

        # is this visible in the main site?
        self.go_to("/")
        self.client.find_element_by_xpath('//*[@name="q"]').send_keys(title + '\n')

        self.client.find_element_by_css_selector('.panel img')

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

        time.sleep(5)
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
        links = self.client.find_elements_by_css_selector('.item-stub  a:last-of-type')
        self.assertEqual(len(items), len(links))

        links[0].click()

        self.assertIn('items', self.client.current_url)

    def test_omega_can_delete_her_items_from_her_dashboard(self):
        # omega signs in
        self.fail('write this test')

    def test_omega_can_upload_images_to_her_items(self):
        filename = get_a_sample_image_file()

        self.login('omega@email.com', 'password')
        items = self.client.find_elements_by_css_selector('.item-stub')

        # she selects the first one
        item = items[0]
        item.find_element_by_xpath('//a[contains(@href, "update")]').click()

        # she needs to add images, since people like pics.
        images = self.client.find_element_by_id('images')

        # selenium does not support multiple image uploads
        images.send_keys(filename)

        # and then shes done uploading files and then clicks submit.
        self.client.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertNotIn('update', self.client.current_url)
        img = self.client.find_elements_by_xpath('//img')[0]
        self.assertIn('omega', img.get_attribute('src'))
        img.click()

        # get the big picture
        self.client.find_element_by_css_selector('img')
