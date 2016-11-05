from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.conf import settings

from .models import UserProfile

alphanumericu = RegexValidator(
    regex=r'^[0-9a-zA-Z_]*$',
    message='Only alphanumeric characters and underscore are allowed.')


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=20, validators=[alphanumericu])
    email = forms.EmailField(max_length=254, required=True)
    invite_code = forms.CharField(max_length=120)

    class Meta:
        model = User
        fields = ['email', 'username', ]

    def clean_invite_code(self):
        error_message = 'Invalid invite code'
        invite_code = self.cleaned_data.get('invite_code')
        if not invite_code == settings.INVITE_CODE:
            raise forms.ValidationError(error_message)
        return invite_code

    def clean_email(self):
        error_message = 'An user with that email already exists'
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
                raise forms.ValidationError(error_message)
        return email


class UserProfileForm(ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = UserProfile
        exclude = ['is_enabled_exchange', 'user']
