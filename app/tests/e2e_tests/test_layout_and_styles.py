from app.tests.test_base import SeleniumTest
import time


class StyleTests(SeleniumTest):

    def test_check_styles(self):

        self.client.get('{}/{}'.format(self.server_url, 'sheets'))
        time.sleep(10)

        # omega gets on the computer and logs into sheetswap
        self.client.get('{}/'.format(self.server_url))

        # the page loads and he sees that the input box is encapsulated
        # in a div with a jumbotron class,
        jumbotron = self.client.find_element_by_css_selector('.jumbotron')

        # and this div is centered
        self.assertAlmostEqual(jumbotron.location['x'] + jumbotron.size['width']/2,
                               self.client.get_window_size()['width']/2,
                               delta=6)

        # he also notices that the text is centered as well
        h1_text = jumbotron.find_element_by_tag_name('h1')

        self.assertAlmostEqual(h1_text.location['x'] + h1_text.size['width']/2,
                               self.client.get_window_size()['width']/2,
                               delta=6)

        # on the upper left hand the logo for the site is prominently displayed
        brand = self.client.find_element_by_css_selector('.navbar-brand')

        self.assertEqual(brand.text, 'SheetSwap')

