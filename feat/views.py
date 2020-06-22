import ast

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
import re
from urllib.request import urlopen
import json

from feat.converter.converter import CookingConverter
from feat.forms import RegisterAsConsumerForm, RegisterAsProviderForm, ConsumerProfileForm, ProviderProfileForm, \
    CreateRecipeForm, CreateMenuForm, CommentForm
from feat.models import Recipe, Menu, Comment


class HomeView(TemplateView):
    template_name = "index.html"


class UserHomeView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        username = request.user.username
        recipes = Recipe.objects.filter(created_by__username=username).order_by('created_at').reverse()
        menus = Menu.objects.filter(created_by__username=username).order_by('created_at').reverse()
        rlikes = Recipe.objects.filter(recipelike__cprofiles__user_id=request.user.id).order_by('created_at').reverse()[:10]
        mlikes = Menu.objects.filter(menulike__cprofiles__user_id=request.user.id).order_by('created_at').reverse()[:10]
        return render(request, "user_home.html", {'recipes': recipes, 'menus': menus, 'rlikes': rlikes, 'mlikes': mlikes})


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

            # adapter: string -> ingredient model
            ingredients_input = form.cleaned_data.get('ingredients')
            #Ex: Tomatoes, grape, raw(321360):2;
            pattern = r'([\w*(,\s)?]+)\(([0-9]*)\)\:([\w*(,\s)?]+)\:([0-9]*)\;'
            r = re.compile(pattern)
            ingredients_list = r.findall(ingredients_input)
            #for i in ingredients_list:
            #    ingredients.append(Ingredient())
            # Make a GET request to retrieve details about the food item.
            api_key = "uHpZNeQkPBjLCcnybhVSTcdzjXt6wgNohqA7gRQu"
            nutritional_value = {
                "Energy": 0,
                "Protein": 0,
                "Carbohydrates": 0,
                "Total lipid (fat)": 0,
                "Minerals": 0,
                "Vitamins and Other Components": 0,
                "Water": 0
            }
            for i in ingredients_list:
                food_id = i[1]
                unit = i[2]
                quantity = int(i[3])
                url = "https://api.nal.usda.gov/fdc/v1/food/{}?api_key={}".format(food_id, api_key)
                serialized_data = urlopen(url).read()
                # check the response status
                data = json.loads(serialized_data)
                # check whether the fields accessed here exist in the first place
                portions = data["foodPortions"]
                for portion in portions:
                    if portion["measureUnit"]["name"] == unit:
                        weight = portion["gramWeight"]
                nutrients = data["foodNutrients"]
                for n in nutrients:
                    nutrient_name = n["nutrient"]["name"]
                    #nutrient_value = n["nutrient"]["rank"]
                    if nutrient_name in nutritional_value:
                        # try:
                        #     nutrient_value = n["amount"]
                        #     nutrient_unit = n["nutrient"]["unitName"]
                        #     # should kJ always be ignored? or is there a case in which only this is given instead of kcal?
                        #     if nutrient_unit.lower() == "kj":
                        #         continue
                        #     nutrient_value = CookingConverter().to_standard(nutrient_value, nutrient_unit, nutrient_name)
                        # except KeyError:
                        #     print("Nutrient amount/unit: '", nutrient_name, "' could not be found for food item: '", food_id, "'.")
                        #     nutrient_value = 0

                        try:
                            # nutritional value per 100g
                            nutrient_value = n["amount"]

                            nutrient_unit = n["nutrient"]["unitName"]
                            # should kJ always be ignored? or is there a case in which only this is given instead of kcal?
                            if nutrient_unit.lower() == "kj":
                                continue

                        except KeyError:
                            print("Nutrient amount/unit: '", nutrient_name, "' could not be found for food item: '", food_id, "'.")
                            nutrient_value = 0

                        nutritional_value[nutrient_name] += quantity * weight * nutrient_value / 100
                # for n in nutrients:
                #     nutrient_name = n["nutrient"]["name"]
                #     nutrient_value = n["nutrient"]["rank"]
                #     if nutrient_name == "Energy":
                #         # check whether cal or kcal or some other unit is used
                #         kcal = nutrient_value
                #     elif nutrient_name == "Protein":
                #         # check whether g or kg or some other unit is used
                #         protein = nutrient_value
                #     elif nutrient_name == "Carbohydrates":
                #         ch = nutrient_value
                #     elif nutrient_name == "Minerals":
                #         min = nutrient_value
                #     elif nutrient_name == "Vitamins and Other Components":
                #         vit = nutrient_value
            #nutritional_value_str = json.dumps(nutritional_value)

            description = form.cleaned_data.get('description')
            instructions = form.cleaned_data.get('instructions')
            difficulty = form.cleaned_data.get('difficulty')
            prepared_in = form.cleaned_data.get('prepared_in')
            image_link = form.cleaned_data.get('image_link')
            if image_link == "":
                image_link = "https://raw.githubusercontent.com/heobu/swe573/feature/posts-like-dislike-follow/feat/static/assets/images/eco-slider-img-1.jpg"
            #form.save(commit=True)
            Recipe.objects.create(created_by=created_by, title=title, ingredients=ingredients_input, nutritional_value=nutritional_value, description=description, instructions=instructions, difficulty=difficulty, prepared_in=prepared_in, image_link=image_link)
            return redirect('user_home')
        else:
            return render('create-recipe')

class RecipeView(View, LoginRequiredMixin):
    def get(self, request, id=None):
        #recipe = Recipe.objects.all()[0]#filter(id=id)
        recipe = Recipe.objects.get(id=id)
        form = CommentForm()
        return render(request, "recipe-detail.html", {'recipe': recipe, 'form': form})

    # , recipe=None
    def post(self, request, id=None):
        form = CommentForm(request.POST, instance=request.user)
        if form.is_valid():
            created_by = request.user
            recipe = Recipe.objects.get(id=id)
            content = form.cleaned_data.get('content')
            #recipe = form.cleaned_data.get('recipe')
            Comment.objects.create(created_by=created_by, content=content, recipe=recipe)
            #return redirect('user_home')
            return redirect('/recipe/detail/{}'.format(id))
        else:
            return render('create-menu')



class MenuCreateView(View, LoginRequiredMixin):

    def get(self, request):
        form = CreateMenuForm()
        recipes = Recipe.objects.filter().order_by('title')
        return render(request, "create-menu.html", {'form': form, 'recipes': recipes})

    def post(self, request):
        form = CreateMenuForm(request.POST, instance=request.user)
        if form.is_valid():
            created_by = request.user
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            image_link = form.cleaned_data.get('image_link')

            # adapter: string -> ingredient model
            food_items_input = form.cleaned_data.get('food_items')
            #Ex: Recipe Title([recipe_id]]):[quantity];
            pattern = r'([\w*(,\s)?]+)\(([0-9]*)\)\:([0-9]*)\;'
            r = re.compile(pattern)
            food_items = r.findall(food_items_input)
            menu_nutritional_value = {
                "Energy": 0,
                "Protein": 0,
                "Carbohydrates": 0,
                "Total lipid (fat)": 0,
                "Minerals": 0,
                "Vitamins and Other Components": 0,
                "Water": 0
            }
            for i in food_items:
                food_id = i[1]
                quantity = int(i[2])

                # food item is not a recipe
                # Retrieve information from USDA for food items.

                # food item is a recipe
                recipe_nutritional_value_str = Recipe.objects.get(id=food_id).nutritional_value
                recipe_nutritional_value = ast.literal_eval(recipe_nutritional_value_str)
                for nutrient_name, nutrient_value in recipe_nutritional_value.items():
                    if nutrient_name in menu_nutritional_value:
                        menu_nutritional_value[nutrient_name] += quantity * nutrient_value

            #form.save(commit=True)
            if image_link == "":
                image_link = "https://raw.githubusercontent.com/heobu/swe573/feature/posts-like-dislike-follow/feat/static/assets/images/eco-slider-img-1.jpg"
            Menu.objects.create(created_by=created_by, title=title, description=description, food_items=food_items, nutritional_value=menu_nutritional_value, image_link=image_link)
            return redirect('user_home')
        else:
            return render('create-menu')

class MenuView(View, LoginRequiredMixin):
    def get(self, request, id=None):
        #recipe = Recipe.objects.all()[0]#filter(id=id)
        menu = Menu.objects.get(id=id)
        return render(request, "menu-detail.html", {'menu': menu})


class SearchRecipeView(View, LoginRequiredMixin):
    def get(self, request, contains=None):
        keyword = request.GET.get('contains', '')
        if keyword != '':
            recipes = Recipe.objects.filter(title__contains=keyword) |\
                     Recipe.objects.filter(description__contains=keyword) |\
                     Recipe.objects.filter(ingredients__contains=keyword) |\
                     Recipe.objects.filter(instructions__contains=keyword)
        else:
            recipes = Recipe.objects.all()

        return render(request, "recipe-search-results.html", {'recipes': recipes, 'keyword': keyword})


class SearchMenuView(View, LoginRequiredMixin):
    def get(self, request, contains=None):
        keyword = request.GET.get('contains', '')
        if keyword != '':
            menus = Menu.objects.filter(title__contains=keyword) |\
                     Menu.objects.filter(description__contains=keyword)
        else:
            menus = Menu.objects.all()

        return render(request, "menu-search-results.html", {'menus': menus, 'keyword': keyword})
