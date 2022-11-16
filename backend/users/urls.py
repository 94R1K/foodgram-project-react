from django.urls import include, path

from .views import SubscribeView, SubscriptionViewSet

urlpatterns = [
    path('users/subscriptions/', SubscriptionViewSet.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:pk>/subscribe/', SubscribeView.as_view()),
]
