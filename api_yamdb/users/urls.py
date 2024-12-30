from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

v1_router = DefaultRouter()
v1_router.register('', UserViewSet, basename='user')

urlpatterns = [
    path('', include(v1_router.urls)),
]
