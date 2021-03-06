"""
    To run tests:
    python manage.py test apps.main
"""

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from apps.main.views import home


class homeTest(TestCase):

    def test_root_url_resolves_to_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_returns_correct_html(self):
        request = HttpRequest()
        response = home(request)
        html = response.content.decode('utf8')

        self.assertIn('<title>Algoraise: Project Avalon</title>', html)
