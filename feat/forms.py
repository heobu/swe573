from django import forms
from django.contrib.auth.forms import UserCreationForm

from feat.models import User, ConsumerProfile, ProviderProfile, Recipe, Menu, Comment


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
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class RegisterAsProviderForm(UserCreationForm):
    email = forms.EmailField(help_text='Email')
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CreateRecipeForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput())
    image_link = forms.URLField(required=False)

    class Meta:
        model = Recipe
        fields = ('title', 'ingredients', 'description', 'instructions', 'difficulty', 'prepared_in', 'image_link')


class CreateMenuForm(forms.ModelForm):
    image_link = forms.URLField(required=False)

    class Meta:
        model = Menu
        fields = ('title', 'description', 'food_items', 'image_link')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
