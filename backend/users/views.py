from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser, Follow
from .serializers import (CurrentUserSerializer, FollowListSerializer,
                          UserFollowSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer
    permission_classes = (AllowAny, )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowView(views.APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, following_id):
        user = request.user
        data = {
            'following': following_id,
            'user': user.id
            }
        serializer = UserFollowSerializer(
            data=data,
            context={'request': request}
            )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, following_id):
        user = request.user
        following = get_object_or_404(CustomUser, id=following_id)
        Follow.objects.filter(user=user, following=following).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FollowListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        request = self.request
        context.update({'request': request})
        return context

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(following__user=user)
