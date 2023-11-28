from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",  "password1", "password2", "Balance")

def save(self, commit=True):
    user = super(SignUpForm, self).save(commit=False)
    user.email = self.cleaned_data['email']
    user.Balance = self.cleaned_data['Balance']
    if commit:
        user.save()
    return user

