from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View

from feat.forms import RegisterAsConsumerForm, RegisterAsProviderForm, ConsumerProfileForm, ProviderProfileForm, \
    CreateRecipeForm
from feat.models import Recipe


class HomeView(TemplateView):
    template_name = "index.html"


class UserHomeView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        username = request.user.username
        recipes = Recipe.objects.filter(created_by__username=username).order_by('created_at')
        return render(request, "user_home.html", {'recipes': recipes})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"


class Logout(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect('home')


class ChangePasswordView(View):

    def get(self, request):
        form = PasswordResetForm()
        return render(request, "custom/change_password.html", {'form': form})

    def post(self, request):
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            return redirect('login')
        else:
            return render(request, "custom/change_password.html", {'form': form})


class LoginView(View):

    def get(self, request):
        form = AuthenticationForm()
        return render(request, "pages/login.html", {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user_home')
        else:
            return render(request, "pages/login.html", {'form': form})


class RegisterAsConsumerView(View):

    def get(self, request):
        form = RegisterAsConsumerForm()
        profile_form = ConsumerProfileForm()
        return render(request, "pages/sign-up.html", {'form': form, 'profile_form': profile_form})

    def post(self, request):
        form = RegisterAsConsumerForm(request.POST)
        profile_form = ConsumerProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.is_consumer = True
            user.save()
            user.consumer_profile.date_of_birth = profile_form.cleaned_data.get('date_of_birth')
            user.consumer_profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user_home')
        else:
            return redirect('pages/sign-up.html')


class RegisterAsProviderView(View):

    def get(self, request):
        form = RegisterAsProviderForm()
        profile_form = ProviderProfileForm()
        return render(request, "pages/sign-up.html", {'form': form, 'profile_form': profile_form})

    def post(self, request):
        form = RegisterAsProviderForm(request.POST)
        profile_form = ProviderProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.is_provider = True
            user.save()
            user.provider_profile.location = profile_form.cleaned_data.get('location')
            user.provider_profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user_home')
        else:
            return redirect('pages/sign-up.html')

class RecipeCreateView(View, LoginRequiredMixin):

    def get(self, request):
        form = CreateRecipeForm()
        return render(request, "create-recipe.html", {'form': form})

    def post(self, request):
        form = CreateRecipeForm(request.POST, instance=request.user)
        if form.is_valid():
            created_by = request.user
            title = form.cleaned_data.get('title')
            ingredients = form.cleaned_data.get('ingredients')
            description = form.cleaned_data.get('description')
            difficulty = form.cleaned_data.get('difficulty')
            prepared_in = form.cleaned_data.get('prepared_in')
            #form.save(commit=True)
            Recipe.objects.create(created_by=created_by, title=title, ingredients=ingredients, description=description, difficulty=difficulty, prepared_in=prepared_in)
            return redirect('user_home')
        else:
            return render('create-recipe')
