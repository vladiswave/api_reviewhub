from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, UserProfileViewSet

v1_router = DefaultRouter()
v1_router.register('', UserViewSet, basename='user')

urlpatterns = [
    path(
        'me/',
        UserProfileViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update'
        }),
        name='user-profile'
    ),
    path('', include(v1_router.urls)),
]
