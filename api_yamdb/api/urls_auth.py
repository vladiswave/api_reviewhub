from django.urls import path

from .views import (CustomTokenObtainPairView, UserRegistrationView,)

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token'),
]
