from app.tests.test_base import SeleniumTest
import time


class SampleCase(SeleniumTest):

    def test_go_to_root(self):
        self.client.get('http://localhost:5000/')

        e = self.client.find_element_by_tag_name('h1')

        self.assertIn('Trade', e.text)
