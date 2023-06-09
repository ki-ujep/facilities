from django.test import TestCase, RequestFactory
from django.urls import reverse

from client.views import search_result

class SearchViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_search_sql_injection(self):
        request = self.factory.get(reverse('search_result'), {'query': "' OR 1=1; --"})
        response = search_result(request)
        self.assertEqual(response.status_code, 200)
        # You should not find any record if SQL injection attempts are properly handled

    def test_search_long_input(self):
        long_query = 'a' * 10000  # Some arbitrarily large number
        request = self.factory.get(reverse('search_result'), {'query': long_query})
        response = search_result(request)
        self.assertEqual(response.status_code, 200)
