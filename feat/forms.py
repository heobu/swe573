from django import forms
from django.contrib.auth.forms import UserCreationForm

from feat.models import User, ConsumerProfile, ProviderProfile

class ConsumerProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(help_text='YYYY-MM-DD')

    class Meta:
        model = ConsumerProfile
        fields = ('date_of_birth',)

class ProviderProfileForm(forms.ModelForm):
    location = forms.CharField(help_text='Location')

    class Meta:
        model = ProviderProfile
        fields = ('location',)

class RegisterAsConsumerForm(UserCreationForm):
    email = forms.EmailField(help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class RegisterAsProviderForm(UserCreationForm):
    email = forms.EmailField(help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
