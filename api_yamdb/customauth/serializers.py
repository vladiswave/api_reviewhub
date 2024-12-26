from rest_framework import serializers
from users.models import CustomUser
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей без аутентификации."""

    email = serializers.EmailField(
        max_length=254,
        allow_blank=False,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Username должен состоять только из букв, цифр '
                'и символов @.+-_'
            ),
            UniqueValidator(
                queryset=CustomUser.objects.all(),
                message='Такой Username уже занят.'
            )
        ]
    )
    role = serializers.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        default='user',
        write_only=True
    )

    def validate(self, data):
        username = data.get('username')
        if username == 'me':
            raise serializers.ValidationError(
                'Username "me" использовать нельзя.'
            )
        return data

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')
