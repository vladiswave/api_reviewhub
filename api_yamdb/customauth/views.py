from rest_framework.response import Response
from users.models import CustomUser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from .utils import generate_and_send_confirmation_code
from users.serializers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny


class UserRegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')

        try:
            user = CustomUser.objects.get(username=username, email=email)
            generate_and_send_confirmation_code(user)
        except ObjectDoesNotExist:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            generate_and_send_confirmation_code(user)

        return Response({
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Invalid username or confirmation code.')

        if user.confirmation_code != confirmation_code:
            raise AuthenticationFailed('Invalid username or confirmation code.')

        token = AccessToken.for_user(user)
        return Response({
            'access': str(token),
        }, status=status.HTTP_200_OK)
