from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm


class SignUpForm(forms.Form):

    """ Defines the sign up form fields and input handling.
        NOTE: Cleaning the input fields removes potential code input from
        the user. """

    username = forms.CharField(label='Username', min_length=4,
                               max_length=150)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput)
    regkey = forms.CharField(label='Registration key')

    class Meta:

        """ Specifies the fields related to the form. """

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            )

    def clean_username(self):
        """ Cleans and checks username does not already exist. """

        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError('Username already exists.')
        return username

    def clean_email(self):
        """ Cleans email and checks email does not already exist. """

        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError('Email already exists.')
        return email

    def clean_password2(self):
        """ Cleans and checks password match. """

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.")

        return password2

    def clean_regkey(self):
        """ Clean register key and checks that it matches the secret key. """

        regkey = self.cleaned_data.get('regkey')
        if regkey != '1a4bCddeJk9mt':
            raise ValidationError('Incorrect registration key.')
        return regkey

    def save(self, commit=True):
        """ Creates user if field inputs are all valid. """

        user = User.objects.create_user(self.cleaned_data['username'],
                self.cleaned_data['email'],
                self.cleaned_data['password1'])
        return user


class EditProfileForm(UserChangeForm):

    """ Form for user to edit their profile. """

    class Meta:

        """ Specifies the fields the user can edit. """

        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
