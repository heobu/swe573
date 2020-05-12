from django.urls import include, path
from rest_framework import routers
from . import api_views

router = routers.DefaultRouter()
router.register(r'consumer_profile', api_views.ConsumerProfileViewSet)
router.register(r'provider_profile', api_views.ProviderProfileViewSet)
router.register(r'recipe_create', api_views.RecipeCreateViewSet)
router.register(r'menu_create', api_views.MenuCreateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]