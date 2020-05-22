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


# class RecipeLikeViewSet(viewsets.ModelViewSet):
#     queryset = RecipeLike.objects.filter(id=id).update(is_liked=True)
#     serializer_class = RecipeLikeSerializer
#
#     def update(self, instance, *args, **kwargs):
#         instance.is_liked = True
#
# class MenuLikeViewSet(viewsets.ModelViewSet):
#     queryset = MenuLike.objects.get(id=id)
#     serializer_class = MenuLikeSerializer

# class UpdateRecipeLikeRetrieveViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
#     #lookup_field = 'recipeId'
#     queryset = RecipeLike.objects.all()
#     #queryset = RecipeLike.objects.get_or_create()
#     serializer_class = RecipeLikeSerializer

#mixins.UpdateModelMixin,
class UpdateRecipeLikeRetrieveViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    #lookup_url_kwarg = "recipe_id"
    queryset = RecipeLike.objects.all()
    #queryset = RecipeLike.objects.filter(recipe_id=recipe_id).update()
    serializer_class = RecipeLikeSerializer

    @action(methods=['get'], detail=True, url_path='toggle', url_name='toggle')
    #def toggle(self, instance, *args, **kwargs):
    def toggle(self, request, pk=None):
        print("huuuuu------------------", pk)
        ##recipe_id = self.kwargs.get(self.lookup_url_kwarg)
        #likes = RecipeLike.objects.filter(recipe_id=pk)
        #print(len(likes))
        ##like = RecipeLike.objects.get(recipe_id=pk)
        ##like.cprofiles
        #cprofiles = ConsumerProfile.objects.filter(recipelike__cprofiles__user_id=request.user.id)
        like = RecipeLike.objects.get(recipe_id=pk)
        try:
            print("Unliking recipe")
            cprofile = ConsumerProfile.objects.get(recipelike__cprofiles__user_id=request.user.id)
            like.cprofiles.remove(cprofile)
        #print(cprofile)
        #if cprofile is None:
        except ConsumerProfile.DoesNotExist:
            print("Liking recipe")
            cprofile = ConsumerProfile.objects.get(user_id=request.user.id)
            like.cprofiles.add(cprofile)

        #print(request.user.id)
        #likes.update_or_create(kwargs)
        return HttpResponse(status=200)

    # queryset = RecipeLike.objects.filter(recipe_id=recipe_id).update()
    # self.update(instance, *args, **kwargs)
    # self.update-partial(instance, *args, **kwargs)