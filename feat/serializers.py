from django.contrib.auth.models import User
from rest_framework import serializers

from feat.models import ConsumerProfile, ProviderProfile, Recipe, Menu


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
        #fields = ('title', 'ingredients', 'description', 'created_by', 'created_at', 'difficulty', 'prepared_in')
        fields = ('title', 'ingredients', 'description', 'difficulty', 'prepared_in')

class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menu
        fields = ('title', 'food_items', 'nutritional_value', 'created_at')
