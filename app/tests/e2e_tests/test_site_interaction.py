from app.tests.test_base import SeleniumTest
import time


class SiteTests(SeleniumTest):

    def test_search(self):
        # mozart logs into the site
        self.go_to('/')

        # hmm lets see what is here
        q = self.client.find_element_by_id('q_box')

        q.send_keys('a')
        q.submit()

        # there are sheets available!
        sheets_a = self.client.find_elements_by_class_name('item-stub')

        # he tries to break the site by seeing if search is case insensitive and space impervious
        self.go_to('/')
        q = self.client.find_element_by_id('q_box')
        q.send_keys('A  ')
        time.sleep(5)
        q.submit()

        sheets_A = self.client.find_elements_by_class_name('item-stub')

        # the search returned the same results
        self.assertEqual(len(sheets_a), len(sheets_A))


