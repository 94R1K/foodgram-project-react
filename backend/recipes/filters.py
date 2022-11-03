from django_filters import rest_framework as filters

from tags.models import Tag
from .models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug'
        )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
        )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
        )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart'
            )

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(favorites__user=user)
        return Recipe.objects.all()

    def get_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(purchases__user=user)
        return Recipe.objects.all()


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
        )

    class Meta:
        model = Ingredient
        fields = (
            'name',
            )
