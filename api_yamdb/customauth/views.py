from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from customauth.serializers import UserRegistrationSerializer
from customauth.utils import generate_and_send_confirmation_code
from users.models import CustomUser


class UserRegistrationView(APIView):
    """Вьюсет регистрации пользователей."""

    permission_classes = (AllowAny,)

    def post(self, request):
        user = CustomUser.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).first()
        if not user:
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

        generate_and_send_confirmation_code(user)

        return Response({
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Вьюсет для выпуска токена."""

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        if not username or not confirmation_code:
            raise ValidationError(
                'Требуется заполнить поля "username" и "confirmation_code".'
            )

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise NotFound('Проверьте username.')

        if user.confirmation_code != confirmation_code:
            raise ValidationError('Неправильный код.')

        return Response({
            'access': str(AccessToken.for_user(user)),
        }, status=status.HTTP_200_OK)
