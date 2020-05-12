from rest_framework import viewsets

from feat.models import ConsumerProfile, ProviderProfile, Recipe, Menu
from feat.serializers import ConsumerProfileSerializer, ProviderProfileSerializer, RecipeSerializer, MenuSerializer


class ConsumerProfileViewSet(viewsets.ModelViewSet):
    queryset = ConsumerProfile.objects.all()
    serializer_class = ConsumerProfileSerializer

class ProviderProfileViewSet(viewsets.ModelViewSet):
    queryset = ProviderProfile.objects.all()
    serializer_class = ProviderProfileSerializer

class RecipeCreateViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class MenuCreateViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer