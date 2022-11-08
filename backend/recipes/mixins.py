from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from .models import Recipe


class CustomMixin:
    serializer_class = None
    model_class = None

    def get(self, request, recipe_id):
        user = request.user.id
        data = {
            'recipe': recipe_id,
            'user': user
            }
        context = {'request': request}
        serializer = self.serializer_class(
            data=data,
            context=context,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        model = self.model_class
        recipe = get_object_or_404(Recipe, id=recipe_id)
        model.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
