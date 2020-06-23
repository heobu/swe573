from django.contrib.auth.models import User
from rest_framework import serializers

from feat.models import ConsumerProfile, ProviderProfile, Recipe, Menu, RecipeLike, MenuLike, DailyIntakeFromRecipe


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ConsumerProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConsumerProfile
        fields = ('date_of_birth',)


class ProviderProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = ('location',)


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = ('title', 'ingredients', 'description', 'instructions', 'difficulty', 'prepared_in')


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menu
        fields = ('title', 'description', 'food_items', 'nutritional_value', 'created_at')


class RecipeLikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecipeLike
        fields = ('recipe', 'cprofiles')


class MenuLikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MenuLike
        fields = ('menu', 'cprofiles')


class DailyIntakeFromRecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DailyIntakeFromRecipe
        fields = ('intake_at',)
