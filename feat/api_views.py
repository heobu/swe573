from functools import partial

from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from feat.models import ConsumerProfile, ProviderProfile, Recipe, Menu, RecipeLike, MenuLike
from feat.serializers import ConsumerProfileSerializer, ProviderProfileSerializer, RecipeSerializer, MenuSerializer, \
    RecipeLikeSerializer, MenuLikeSerializer


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


# Customers can like/unlike recipes. Can providers?
class UpdateRecipeLikeRetrieveViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = RecipeLike.objects.all()
    serializer_class = RecipeLikeSerializer

    @action(methods=['get'], detail=True, url_path='toggle', url_name='toggle')
    def toggle(self, request, pk=None):
        like = RecipeLike.objects.get(recipe_id=pk)
        try:
            print("Unliking recipe")
            cprofile = ConsumerProfile.objects.get(recipelike__cprofiles__user_id=request.user.id)
            like.cprofiles.remove(cprofile)
        except ConsumerProfile.DoesNotExist:
            print("Liking recipe")
            cprofile = ConsumerProfile.objects.get(user_id=request.user.id)
            like.cprofiles.add(cprofile)

        return HttpResponse(status=200)


# Customers can like/unlike menus. Can providers?
class UpdateMenuLikeRetrieveViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = MenuLike.objects.all()
    serializer_class = MenuLikeSerializer

    @action(methods=['get'], detail=True, url_path='toggle', url_name='toggle')
    def toggle(self, request, pk=None):
        like = MenuLike.objects.get(menu_id=pk)
        try:
            print("Unliking menu")
            cprofile = ConsumerProfile.objects.get(menulike__cprofiles__user_id=request.user.id)
            like.cprofiles.remove(cprofile)
        except ConsumerProfile.DoesNotExist:
            print("Liking menu")
            cprofile = ConsumerProfile.objects.get(user_id=request.user.id)
            like.cprofiles.add(cprofile)

        return HttpResponse(status=200)
