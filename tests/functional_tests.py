"""
To run tests:
    1. 'cd' into this directory
    2. Type 'pytest functional_tests.py'

To run tests with specific marks:
    'pytest functional_tests.py -v -m <mark_name>'
    e.g. pytest functional_tests.py -v -m redirects

Chromedriver is for MacOS-64 bit version 73 of Google Chrome.
"""
import pytest
from selenium import webdriver   # Browser testing framework

CHROME_PATH = r"./resources/chromedriver.exe"
BROWSER_PATH = 'http://localhost:8000'


@pytest.mark.djangotest
def test_django_installed():
    """ Opens and checks browser to ensure Django package is installed. """
    # Starts up chrome browser - required everytime
    browser = webdriver.Chrome(executable_path=CHROME_PATH)
    browser.get(BROWSER_PATH)
    assert 'Project Avalon' in browser.title
    browser.quit()

def page_test(url, title):
    """ Load page at specificed URL and check title contains 'title'. """ 
    browser = webdriver.Chrome(executable_path=CHROME_PATH)
    browser.get(BROWSER_PATH + url)
    assert title in browser.title
    browser.quit()


@pytest.mark.pagetest
class TestPages:
    def test_home_page(self):
        page_test('', 'Algoraise: Project Avalon')

    def test_login_page(self):
        page_test('/account/login', 'Log in')

    def test_signup_page(self):
        page_test('/account/signup', 'Sign up')

    def test_reset_password_page(self):
        page_test('/account/reset-password', 'Reset password')


@pytest.mark.redirects
class TestRedirects:
    def test_app_page_redirects_to_log_in_page(self):
        page_test('/projectavalon', 'Log in')

    def test_results_page_redirects_to_log_in_page(self):
        """ Securely tested in apps.upload.tests """
        # page_test('/projectavalon/500-data/graph', 'Log in')
        pass

    def test_delete_page_redirects_to_log_in_page(self):
        """ Securely tested in apps.upload.tests """
        # page_test('/projectavalon/507/delete', 'Log in')
        pass

    def test_profile_page_redirects_to_log_in_page(self):
        page_test('/account/profile', 'Log in')

    def test_edit_profile_page_redirects_to_log_in_page(self):
        page_test('/account/profile/edit', 'Log in')

    def test_change_password_page_redirects_to_log_in_page(self):
        page_test('/account/change-password', 'Log in')

    def test_kill_port_page_redirects_to_log_in_page(self):
        page_test('/tensor/kill-port', 'Log in')
