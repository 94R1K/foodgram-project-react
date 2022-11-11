from rest_framework.permissions import BasePermission, IsAuthenticated


class IsOwnerProfile(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff
        )
