from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FavoriteView, IngredientViewSet, RecipeViewSet

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:favorite_id>/favorite/', FavoriteView.as_view()),
]
