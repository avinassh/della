from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

alphanumericu = RegexValidator(
    regex=r'^[0-9a-zA-Z_]*$',
    message='Only alphanumeric characters and underscore are allowed.')


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=20, validators=[alphanumericu])
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', ]

    def clean_email(self):
        error_message = 'An user with that email already exists'
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
                raise forms.ValidationError(error_message)
        return email
