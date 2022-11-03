from django.urls import include, path

from .views import FollowListView, FollowView

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:following_id>/subscribe/', FollowView.as_view()),
    path('users/subscriptions/', FollowListView.as_view()),
]
