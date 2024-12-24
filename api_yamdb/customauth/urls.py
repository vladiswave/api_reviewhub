from django.urls import path

from .views import UserRegistrationView, CustomTokenObtainPairView

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token'),
]
