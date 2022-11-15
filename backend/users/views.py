from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.pagination import CustomPagination

from .models import CustomUser, Subscription
from .serializers import SubscribeSerializer, SubscriptionSerializer


class SubscriptionViewSet(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        request = self.request
        context.update({'request': request})
        return context

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(following__user=user)


class SubscribeView(views.APIView):
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated, )

    def post(self, request, following_id):
        user = request.user
        data = {
            'author': following_id,
            'user': user.id
        }
        serializer = SubscribeSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, following_id):
        user = request.user
        author = get_object_or_404(CustomUser, id=following_id)
        Subscription.objects.filer(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
