from rest_framework.response import Response
from users.models import CustomUser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed, ValidationError, NotFound
from .utils import generate_and_send_confirmation_code
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import AllowAny


class UserRegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')

        user = CustomUser.objects.filter(username=username, email=email).first()

        if user:
            generate_and_send_confirmation_code(user)
        else:
            serializer = UserRegistrationSerializer(data=request.data)
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

        if not username or not confirmation_code:
            raise ValidationError("Заполните поля 'username' и 'confirmation_code'.")

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise NotFound('Проверьте username.')

        if user.confirmation_code != confirmation_code:
            raise ValidationError('Неправильный код.')

        token = AccessToken.for_user(user)
        return Response({
            'access': str(token),
        }, status=status.HTTP_200_OK)
