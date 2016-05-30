from flask import url_for
from app.tests.test_base import AppTest


class SiteTests(AppTest):

    def test_queries_should_be_case_space_insensitive(self):
        response_a = self.client.get(url_for('main.search_results'),
                                     query_string={'q': 'a'},
                                     follow_redirects=True)
        response_A = self.client.get(url_for('main.search_results'),
                                     query_string={'q': 'A   '},
                                     follow_redirects=True)

        self.assertIn('Adele', response_A.get_data(as_text=True))
        self.assertIn('Adele', response_a.get_data(as_text=True))
        self.assertIn('Piano', response_A.get_data(as_text=True))
        self.assertIn('Piano', response_a.get_data(as_text=True))
