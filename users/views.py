#Django Imports 
from django.shortcuts import render, redirect, get_object_or_404
from allauth.account.views import LoginView, SignupView, LogoutView, PasswordSetView, PasswordChangeView, PasswordResetView, EmailView, ConfirmEmailView
from allauth.socialaccount.views import ConnectionsView

#Project File Imports
from .models import User


# Views
def view_profile(request):
    return render(request, "users/profile.html")