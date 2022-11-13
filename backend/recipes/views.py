import datetime

from django.db.models import Sum
from django.shortcuts import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from .filters import IngredientFilter, RecipeFilter
from .mixins import CustomMixin
from .models import (Favorite, Ingredient, Recipe,
                     ShoppingList)
from .permissions import IsOwnerOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeFullSerializer, RecipeSerializer,
                          ShoppingListSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsOwnerOrReadOnly, ]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 6
    filter_backends = [DjangoFilterBackend, ]
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return RecipeFullSerializer
        return RecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        request = self.request
        context.update({'request': request})
        return context


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    pagination_class = None
    filter_backends = [DjangoFilterBackend, ]
    filter_class = IngredientFilter


class FavoriteView(CustomMixin, views.APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FavoriteSerializer
    model_class = Favorite


class ShoppingListView(CustomMixin, views.APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ShoppingListSerializer
    model_class = ShoppingList


class DownloadShoppingCartView(views.APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        recipes = Recipe.objects.filter(
            is_favorited__user=user,
            is_favorited__is_in_shopping_cart=True
        )
        ingredients = recipes.values(
            'ingredients__name',
            'ingredients__measurement_unit__name').order_by(
            'ingredients__name').annotate(
            ingredients_total=Sum('ingredient_amounts__amount')
        )
        shopping_list = {}
        for item in ingredients:
            name = item.get('ingredients__name')
            amount = str(item.get('ingredients_total'))
            measurement_unit = item['ingredients__measurement_unit__name']
            shopping_list[name] = {
                'measurement_unit': measurement_unit,
                'amount': amount
            }
        main_list = ([f"* {item}:{value['amount']}"
                      f"{value['measurement_unit']}\n"
                      for item, value in shopping_list.items()])
        today = datetime.date.today()
        main_list.append(f'\n From Foodgram with love, {today.year}')
        response = HttpResponse(main_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="BuyList.txt"'
        return response
