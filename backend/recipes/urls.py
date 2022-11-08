from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShoppingCartView, FavoriteView, IngredientViewSet,
                    RecipeViewSet, ShoppingListView)

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'recipes/download_shopping_cart/',
        DownloadShoppingCartView.as_view()),
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteView.as_view()),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        ShoppingListView.as_view()),
]
