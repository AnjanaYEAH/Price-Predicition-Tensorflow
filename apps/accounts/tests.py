"""
    To run all tests:
    python manage.py test apps.accounts.tests
    
    To run specific test cases:
    python manage.py test apps.accounts.tests.<name of test class>
"""
from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.views import Login, SignUp
from apps.accounts.forms import EditProfileForm, SignUpForm
from django.contrib.auth.models import User


TOO_LONG_USERNAME = "edxbtmawhihixuiuyddereplzogqdzkveihnhqcbtbelhxzrtceuoivwaygdpgqfcjpdfsneknmemmltlrrudzrizcvdiotnbwpfimnqmfvxshsiznianitzhjgpgwgvatfpongmebdyrwwfwwvjeszduirsbsmf"


class LogInTest(TestCase):

    def setUp(self):
        """ Initialises user for testing. Runs before tests. """
        test_user = User.objects.create_user(username='test-username', password='test-password')
    
    def test_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('upload:drag_and_drop'))
        self.assertRedirects(response, '/account/login/')
        
        response = self.client.get(reverse('accounts:view_profile'))
        self.assertRedirects(response, '/account/login/')
    
        response = self.client.get(reverse('accounts:edit_profile'))
        self.assertRedirects(response, '/account/login/')
        
        response = self.client.get(reverse('accounts:change_password'))
        self.assertRedirects(response, '/account/login/')
    
        response = self.client.get(reverse('tensor:script2'))
        self.assertRedirects(response, '/account/login/')
    
    
    def test_log_in_for_valid_user(self):
        login = self.client.login(username='test-username', password='test-password')
        response = self.client.get(reverse('upload:drag_and_drop'))

        self.assertEqual(str(response.context['user']), 'test-username')
        self.assertEqual(response.status_code, 200)

    def test_log_in_for_invalid_user(self):
        login = self.client.login(username='invalid-username', password='invalid-password')
        response = self.client.get(reverse('accounts:login'))
    
        self.assertNotEqual(str(response.context['user']), 'invalid-username')
        self.assertEqual(response.status_code, 200)
    
    def test_log_in_redirects_for_already_logged_in_user(self):
        login = self.client.login(username='test-username', password='test-password')
        response = self.client.get(reverse('accounts:login'))
    
        self.assertRedirects(response, '/')

    def tearDown(self):
        """ Cleans up database after all tests are complete."""
        User.objects.filter(username='test-username').delete()


def example_sign_up_form(username='test-username', email='test-email@ucl.ac.uk', password1='test-password', password2='test-password', regkey='1a4bCddeJk9mt'):
    form = SignUpForm(data={
                      'username': username,
                      'email': email,
                      'password1': password1,
                      'password2': password2,
                      'regkey': regkey
                      })
    return form

class SignUpFormTest(TestCase):

    def test_sign_up_form_labels(self):
        form = SignUpForm()
        self.assertTrue(form.fields['username'].label == None or form.fields['username'].label == 'Username')
        self.assertTrue(form.fields['email'].label == None or form.fields['email'].label == 'Email')
        self.assertTrue(form.fields['password1'].label == None or form.fields['password1'].label == 'Password')
        self.assertTrue(form.fields['password2'].label == None or form.fields['password2'].label == 'Confirm password')
        self.assertTrue(form.fields['regkey'].label == None or form.fields['regkey'].label == 'Registration key')

    def test_rejected_if_username_is_too_short(self):
        form = example_sign_up_form(username='me')
        self.assertFalse(form.is_valid())
    
    def test_rejected_if_username_is_too_long(self):
        form = example_sign_up_form(username=TOO_LONG_USERNAME)
        self.assertFalse(form.is_valid())
    
    def test_rejected_if_username_already_exists(self):
        test_user = User.objects.create_user(username='already-exists')
        form = example_sign_up_form(username='already-exists')
        self.assertFalse(form.is_valid())
        User.objects.filter(username='already-exists').delete()

    def test_rejected_if_email_already_exists(self):
        test_user = User.objects.create_user(username='sample-username', email='already_exists@ucl.ac.uk')
        form = example_sign_up_form(email='already_exists@ucl.ac.uk')
        self.assertFalse(form.is_valid())
        User.objects.filter(email='already_exists@ucl.ac.uk').delete()

    def test_rejected_if_email_is_invalid(self):
        form = example_sign_up_form(email='not_an_email')
        self.assertFalse(form.is_valid())

    def test_rejected_if_passwords_do_not_match(self):
        form = example_sign_up_form(password1='me', password2='you')
        self.assertFalse(form.is_valid())

    def test_rejected_if_registration_key_is_incorrect(self):
        form = example_sign_up_form(regkey='123')
        self.assertFalse(form.is_valid())


class SignUpFormViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_valid_sign_up_form_submission(self):
        response = self.client.post('/account/signup/', data={
                                    'username': 'test-username',
                                    'email': 'test@ucl.ac.uk',
                                    'password1': 'test-password',
                                    'password2': 'test-password',
                                    'regkey': '1a4bCddeJk9mt'
                                    })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/login/')

    def test_invalid_sign_up_form_submission(self):
        response = self.client.post('/account/signup/', data={
                                    'username': 'hi',
                                    'email': 'test@ucl.ac.uk',
                                    'password1': 'test-password',
                                    'password2': 'test-password',
                                    'regkey': '1a4bCddeJk9mt'
                                    })
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_logged_in_users_are_redirected_to_home_page(self):
        test_user = User.objects.create_user(username='test-username', password='test-password')
        login = self.client.login(username='test-username', password='test-password')
        response = self.client.get('/account/signup/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        User.objects.filter(username='test-user').delete()

    def test_sign_up_page_loads_for_unauthorised_users(self):
        response = self.client.get('/account/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')


class EditProfileFormTest(TestCase):

    def test_sign_up_form_labels(self):
        form = EditProfileForm()
        self.assertTrue(form.fields['email'].label == None or form.fields['email'].label == 'Email address')
        self.assertTrue(form.fields['first_name'].label == None or form.fields['first_name'].label == 'First name')
        self.assertTrue(form.fields['last_name'].label == None or form.fields['last_name'].label == 'Last name')


class EditProfileFormViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        test_user = User.objects.create_user(username='test-username', password='test-password')
    
    def test_edit_profile_page_loads_for_logged_in_users(self):
        login = self.client.login(username='test-username', password='test-password')
        response = self.client.get('/account/profile/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit_profile.html')

    def test_edit_profile_page_redirects_for_unauthorised_users(self):
        login = self.client.login(username='test-username', password='test-password')
        response = self.client.post('/account/profile/edit/',data={'email':'new_email@ucl.ac.uk', 'first_name':'user-first-name', 'last_name':'user-surname'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/profile/')
        self.assertTrue(User.objects.filter(username='test-username', email='new_email@ucl.ac.uk', first_name='user-first-name', last_name='user-surname').exists())
    
    def tearDown(self):
        User.objects.filter(username='test-username').delete()


class ViewProfileViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        test_user = User.objects.create_user(username='test-username', password='test-password')

    def test_view_profile_page_loads_for_authorised_users(self):
        login = self.client.login(username='test-username', password='test-password')
        response = self.client.get('/account/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def tearDown(self):
        User.objects.filter(username='test-username').delete()


class ChangePasswordViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        test_user = User.objects.create_user(username='test-username', password='test-password')

    def test_change_password_page_redirects_to_login_page_for_unauthorised_users(self):
        response = self.client.get('/account/change-password/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/login/')

    def test_change_password_page_loads_for_authorised_users(self):
        login = self.client.login(username='test-username', password='test-password')
        response = self.client.get('/account/change-password/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/change_password.html')

    def test_change_password_form_is_rejected_for_invalid_entry(self):
        login = self.client.login(username='test-username', password='test-password')
        response = self.client.get('/account/change-password/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/account/change-password/', data={
                                    'old_password':'test-password',
                                    'new_password1':'different-password1',
                                    'new_password2':'different-password2'
                                    })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.get(username='test-username').check_password('test-password'))
        self.assertRedirects(response, '/account/change-password/')

    def test_change_password_form_is_accepted_and_password_is_updated_for_valid_entry(self):
        login = self.client.login(username='test-username', password='test-password')
        response = self.client.get('/account/change-password/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/account/change-password/', data={
                                    'old_password':'test-password',
                                    'new_password1':'new-password',
                                    'new_password2':'new-password'
                                    })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.get(username='test-username').check_password('new-password'))
        self.assertRedirects(response, '/account/profile/')

    def tearDown(self):
        User.objects.filter(username='test-username').delete()







