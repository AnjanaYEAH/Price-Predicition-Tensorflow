"""accounts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password,
         name='change_password'),
    path('reset-password/',
         PasswordResetView.as_view(template_name='accounts/reset_password.html'
         , success_url=reverse_lazy('accounts:password_reset_done'),
         email_template_name='accounts/email_template.html'),
         name='password_reset'),
    path('reset-password/done/',
         PasswordResetDoneView.as_view(template_name='accounts/reset_password_done.html'
         ), name='password_reset_done'),
    path('reset-password/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(success_url=reverse_lazy('accounts:password_reset_complete'
         )), name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='accounts/reset_password_complete.html'),
         name='password_reset_complete'),
    ]
