from selenium import webdriver
from app.tests.test_base import SeleniumTest
from models import Trade, Sheetmusic
import time


class TradeTests(SeleniumTest):

    def omega_creates_an_item(self):

        self.other_client = webdriver.Firefox()
        self.other_client.implicitly_wait(3)
        self.login('omega@email.com', 'password', self.other_client)
        self.create_item('symphony #5', 'beethoven', other_client=self.other_client)
        self.other_client.quit()

    def alpha1_requests_omegas_item(self):
        self.other_client = webdriver.Firefox()
        self.other_client.implicitly_wait(3)
        self.login('alpha1@email.com', 'password', self.other_client)
        self.other_client.get("{}/{}".format(self.server_url, 'sheets'))
        panel = self.other_client.find_element_by_xpath('//div[@class="panel panel-default" and '
                                                  'contains(.//a, "symphony #5")]')
        link = panel.find_element_by_tag_name('a')
        link.click()
        item = self.other_client.find_element_by_css_selector('.item-stub')
        item.find_element_by_css_selector('.btn-link').click()
        self.other_client.quit()

        sheetmusic_id = Sheetmusic.query.filter_by(title='symphony #5').one().id
        return Trade.query.filter(Trade.item_to.has(sheetmusic_id=sheetmusic_id)).one().id



    def test_typical_trading_session(self):
        # alpha1 and omega are trading, so have omega create an item
        self.omega_creates_an_item()


        # alpha1 logs in
        self.login('alpha1@email.com', 'password')

        # he needs sheets
        # he sees whats available
        self.client.get("{}/{}".format(self.server_url, 'sheets'))

        time.sleep(5)
        # found something that looks worthwhile
        panel = self.client.find_element_by_xpath('//div[@class="panel panel-default" and '
                                                  'contains(.//a, "symphony #5")]')

        # (copy the title for the next step)
        link = panel.find_element_by_tag_name('a')
        sheet_title = link.text.strip()

        # it is available and only has one copy!
        self.assertIn('1 copy available!', panel.text)

        # he clicks on the link
        link.click()

        # the header informs the user that this indeed is the correct page
        self.assertIn(sheet_title, self.client.find_element_by_tag_name('h1').text)

        # the only copy available shows that its in a clean condition
        item = self.client.find_element_by_css_selector('.item-stub')
        self.assertIn('clean', item.text)

        # it belongs to someone named omega
        self.assertIn('omega', item.text)

        # he requests the trade
        item.find_element_by_css_selector('.btn-link').click()
        # and is taken to his dashboard with the acknowledgement
        success_notification = self.client.find_element_by_css_selector('.alert-success')
        # the acknowledgement contains info about the trade, the member and item of the trade
        self.assertIn('omega', success_notification.text)
        self.assertIn(sheet_title, success_notification.text)
        # he goes off and exercises or something

        # omega logs in (maybe because she got an email or something)
        self.other_client = webdriver.Firefox()
        self.login('omega@email.com', 'password', self.other_client)
        # checks the requests and sees that there is a pending request
        # from alpha1 for her sheetmusic
        self.go_to('dashboard', self.other_client)
        trade_divs = self.other_client.find_elements_by_xpath('//div[contains(@class,"trade-stub") '
                                                'and contains(.//*, "alpha1")]')

        self.assertTrue(any(['symphony #5' in trade.text for trade in trade_divs]))

        # she thinks, hmm let's check out what alpha1 has
        # she clicks on accept and is taken to a trading session
        accept_button = self.other_client\
            .find_element_by_xpath('//button[contains(./span/@class, "accept-trade")]')

        accept_button.click()
        self.assertIn('Trading with', self.other_client.find_element_by_tag_name('h1').text)


        # she finds that alpha1 has great music so requests a trade with
        # him for a particular copy (the first one)
        sheet = self.other_client.find_elements_by_css_selector('.item-stub')[0]
        accept_button = sheet.find_element_by_xpath('//button[contains(./span/@class, "accept-trade")]')
        accept_button.click()

        # she is then taken to a trade success page
        # this page shows that the trade is a success
        success = self.other_client.find_element_by_css_selector('.alert-success')
        self.assertIn('completed', success.text)

        # the addresses of both parties are shown
        addresses = self.other_client.find_elements_by_css_selector('.address')
        self.assertEqual(len(addresses), 2)




    def test_unauthorized_user_cannot_access_a_trade(self):
        # this story is about alpha1, omega, and mary
        # the code for adding and item, requesting a trade is abstracted out since
        # it has already been tested above

        # alpha1 and omega are trading
        self.omega_creates_an_item()
        the_trade_id = self.alpha1_requests_omegas_item()

        # enter mary, she is being sneaky
        self.login('mary@email.com', 'password')

        # she notices that trades are being accessed by numbers ie trades/3
        # she wonders if she can snoop in on some other trade (namely alpha1 and omegas trade)
        # she tries entering in a random number

        self.go_to("trades/{}".format(the_trade_id))

        # she is thwarted by the advanced security machinery
        self.assertIn('dashboard', self.client.current_url)

        # an alert gets raised that tells mary she can't do that
        error = self.client.find_element_by_css_selector('.alert-danger')

        self.assertIn('you are not a part of that trade', error.text.lower())


