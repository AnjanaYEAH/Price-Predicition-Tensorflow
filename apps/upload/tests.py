"""
    To run all tests:
    python manage.py test apps.accounts.tests

    To run specific test cases:
    python manage.py test apps.accounts.tests.<name of test class>
    """
from django.test import TestCase, Client
from django.urls import reverse
from apps.upload.views import UploadView
from apps.upload.forms import UploadForm
from .models import FileUpload


class FileUploadTest(TestCase):

    def test_results_page_redirects_to_log_in_page_for_unauthorised_users(self):
        response = self.client.get(reverse('upload:drag_and_drop'))
        self.assertRedirects(response, '/account/login/')
