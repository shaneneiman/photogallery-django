from allauth.account.forms import SignupForm
from django import forms

class CustomSignUpForm(SignupForm):
    bio = forms.CharField(max_length=100, label="Bio", required=False)
    def save(self, request):
        user = super().save(request)
        user.bio = self.cleaned_data["bio"]
        user.save()
        return user