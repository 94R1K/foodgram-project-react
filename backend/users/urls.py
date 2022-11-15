from django.urls import include, path

from .views import SubscribeView, SubscriptionViewSet

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/', SubscriptionViewSet.as_view()),
    path('users/<int:following_id>/subscribe/', SubscribeView.as_view()),
]
