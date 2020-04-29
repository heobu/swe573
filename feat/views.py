from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
#from django.contrib import messages

from django.views import View

from feat.forms import RegisterAsConsumerForm, RegisterAsProviderForm


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
            #messages.error(request, form.get_invalid_login_error())
            print(form.get_invalid_login_error())
            #return redirect('login')
            return render(request, "login.html", {'form': form})

class RegisterAsConsumerView(View):

    def get(self, request):
        form = RegisterAsConsumerForm()
        return render(request, "register/consumer.html", {'form': form})

    def post(self, request):
        form = RegisterAsConsumerForm(request.POST)
        if form.is_valid():
            form.save()
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
        return render(request, "register/provider.html", {'form': form})

    def post(self, request):
        form = RegisterAsProviderForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user_home')
        else:
            print(form.errors)
            return redirect('register_provider')

"""
    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')

        render(request, "register/consumer.html")
"""
"""
class RegisterView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')
"""
