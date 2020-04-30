from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View

from feat.forms import RegisterAsConsumerForm, RegisterAsProviderForm, ConsumerProfileForm, ProviderProfileForm


class HomeView(TemplateView):
    template_name = "index.html"

class UserHomeView(LoginRequiredMixin, TemplateView):
    template_name = "user_home.html"

class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('home')

class LoginView(View):

    def get(self, request):
        form = AuthenticationForm()
        return render(request, "login.html", {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user_home')
        else:
            print(form.get_invalid_login_error())
            return render(request, "login.html", {'form': form})

class RegisterAsConsumerView(View):

    def get(self, request):
        form = RegisterAsConsumerForm()
        profile_form = ConsumerProfileForm()
        return render(request, "register/consumer.html", {'form': form, 'profile_form': profile_form})

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
            return redirect('register_consumer')

class RegisterAsProviderView(View):

    def get(self, request):
        form = RegisterAsProviderForm()
        profile_form = ProviderProfileForm()
        return render(request, "register/provider.html", {'form': form, 'profile_form': profile_form})

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
            return redirect('register_provider')
