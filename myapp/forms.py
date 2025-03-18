# myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    identifier = forms.CharField(label='Username, Email or Phone Number')

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

class PhoneLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=15)