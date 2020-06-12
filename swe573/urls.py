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

from feat.views import HomeView, RegisterAsConsumerView, RegisterAsProviderView, UserHomeView, LoginView, Logout, \
    ChangePasswordView, ProfileView, RecipeCreateView, RecipeView, MenuCreateView, MenuView, SearchRecipeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="home"),
    path('home', UserHomeView.as_view(), name="user_home"),
    #path('', UserHomeView.as_view(), name="user_home"),
    path('profile', ProfileView.as_view(), name="profile"),
    path('register/consumer', RegisterAsConsumerView.as_view(), name="register_consumer"),
    path('register/provider', RegisterAsProviderView.as_view(), name="register_provider"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', Logout.as_view(), name="logout"),
    path('change_password', ChangePasswordView.as_view(), name="change_password"),
    path('recipe/create', RecipeCreateView.as_view(), name="recipe_create"),
    path('recipe/detail/<int:id>', RecipeView.as_view()),
    path('menu/create', MenuCreateView.as_view(), name="menu_create"),
    path('menu/detail/<int:id>', MenuView.as_view()),
    #path('search/recipe/(?P<contains>\w{0,50})/$', SearchRecipeView.as_view(), name="search_recipe"),
    path('search/recipe', SearchRecipeView.as_view(), name="search_recipe"),
    path('api/', include('feat.api_urls')),

    #path('recipe/edit/<int:id>', RecipeView.as_view()),
    #path('', include('homepage.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/signup/', SignUp.as_view(), name='signup'),
    #path('^recipe/detail(?P<id>[0-9]+)/$', RecipeView.as_view()),#, name="recipe_detail_{}".format()),

]
