from django import forms
from django.contrib.auth.forms import UserCreationForm

from feat.models import User


# from django.contrib.auth.models import User

# class LoginForm(AuthenticationForm):


class RegisterAsConsumerForm(UserCreationForm):
    date_of_birth = forms.DateField(help_text='YYYY-MM-DD')
    email = forms.EmailField(help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'date_of_birth', 'password1', 'password2')
        # fields = ('username', 'email', 'password1', 'password2')


class RegisterAsProviderForm(UserCreationForm):
    location = forms.DateField(help_text='Location')
    email = forms.EmailField(help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'location', 'password1', 'password2')
