from django.urls import include, path
from rest_framework import routers
from . import api_views

router = routers.DefaultRouter()
router.register(r'consumer_profile', api_views.ConsumerProfileViewSet)
router.register(r'provider_profile', api_views.ProviderProfileViewSet)
router.register(r'recipe_create', api_views.RecipeCreateViewSet)
router.register(r'menu_create', api_views.MenuCreateViewSet)
router.register(r'like/recipe', api_views.UpdateRecipeLikeRetrieveViewSet)
#router.register(r'like/recipe/<int:recipe_id>', api_views.UpdateRecipeLikeRetrieveViewSet)
#router.register(r'recipe_like/<int:recipe_id>', api_views.UpdateRecipeLikeRetrieveViewSet)
#router.register(r'like/recipe/(?P<recipe_id>\d+)', api_views.UpdateRecipeLikeRetrieveViewSet)
#router.register(r'like/recipe/id/<int:recipe_id>', api_views.UpdateRecipeLikeRetrieveViewSet)
#router.register(r'like/recipe/{recipeId}', api_views.UpdateRecipeLikeRetrieveViewSet)
#router.register(r'like/recipe/<int:recipeId>', api_views.RecipeLikeViewSet)
#router.register(r'like/menu/<int:id>', api_views.MenuLikeViewSet),

urlpatterns = [
    path('', include(router.urls)),
    #path('like/recipe/<int:recipe_id>', api_views.UpdateRecipeLikeRetrieveViewSet),
    #path('like/menu/<int:menuid>', api_views.MenuLikeViewSet),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]