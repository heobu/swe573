"""swe573 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#from django.contrib.auth.views import LogoutView
from django.urls import path, include

from feat.views import HomeView, RegisterAsConsumerView, RegisterAsProviderView, UserHomeView, LoginView, Logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="home"),
    path('home', UserHomeView.as_view(), name="user_home"),
    path('register/consumer', RegisterAsConsumerView.as_view(), name="register_consumer"),
    path('register/provider', RegisterAsProviderView.as_view(), name="register_provider"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', Logout.as_view(), name="logout"),

    #path('', include('homepage.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/signup/', SignUp.as_view(), name='signup')
]