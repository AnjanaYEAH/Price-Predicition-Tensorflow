from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse  # allows mapping of URLS to app names
from django.views import generic
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from .forms import EditProfileForm, SignUpForm


class Login(LoginView):

    """ Inherits from Django's built-in LoginView, handling GET/POST requests
        on the login page. """

    template_name = 'accounts/login.html'

    def get(
        self,
        request,
        *args,
        **kwargs
        ):
        """ If the user is already logged in: redirect to the home page.
            Else: load the login page. """

        if self.request.user.is_authenticated:
            messages.warning(request, 'You are already logged in.')
            return redirect(reverse('main:home'))
        return super(Login, self).get(request, *args, **kwargs)


class SignUp(generic.CreateView):

    """ Inherits from Django's built-in CreateView, to create a sign up form.
        Handles GET/POST requests for the page. """

    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get(self, request):
        """ Load the appropriate page for the user. """

        if self.request.user.is_authenticated:
            messages.warning(request, 'You are already logged in.')
            return redirect(reverse('main:home'))
        form = self.form_class(None)

        # Send an empty form to the user to fill in

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """ Validate the form and provide feedback. """

        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('accounts:login')

        messages.warning(request,
                         'Invalid form entry. Please correct the highlighted fields.'
                         )
        return render(request, self.template_name, {'form': form})  # invalid entry


def view_profile(request):
    """ Simple view for handling the view profile page. """

    if request.method == 'GET':
        if not request.user.is_authenticated:
            messages.warning(request,
                             'You must log in before you can access your profile.'
                             )
            return redirect(reverse('accounts:login'))
    args = {'user': request.user}

    # Send the user's details to display if logged in

    return render(request, 'accounts/profile.html', args)


def edit_profile(request):
    """ Simple view for handling the edit profile page. """

    if request.method == 'POST':

        # Get specific user's inputted form

        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:view_profile'))
    else:
        if not request.user.is_authenticated:
            messages.warning(request,
                             'You must log in before you can edit your profile.'
                             )
            return redirect(reverse('accounts:login'))
        form = EditProfileForm(instance=request.user)
        args = {'form': form}

        # Send an empty form for the user to edit their details

        return render(request, 'accounts/edit_profile.html', args)


def change_password(request):
    """ Simple view for handling the change password page. """

    if request.method == 'POST':

        # Get specific user's inputted form

        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        if not request.user.is_authenticated:
            messages.warning(request,
                             'You must log in before you can change your password.'
                             )
            return redirect(reverse('accounts:login'))
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)
