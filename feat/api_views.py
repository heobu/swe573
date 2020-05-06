from rest_framework import viewsets

from feat.models import ConsumerProfile, ProviderProfile, Recipe
from feat.serializers import ConsumerProfileSerializer, ProviderProfileSerializer, RecipeSerializer


class ConsumerProfileViewSet(viewsets.ModelViewSet):
    queryset = ConsumerProfile.objects.all()
    serializer_class = ConsumerProfileSerializer

class ProviderProfileViewSet(viewsets.ModelViewSet):
    queryset = ProviderProfile.objects.all()
    serializer_class = ProviderProfileSerializer

class RecipeCreateViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer