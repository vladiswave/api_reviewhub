from rest_framework import serializers
from users.models import CustomUser
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, allow_blank=False,)
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
            )
        ]
    )
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, default='user', write_only=True)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if username and CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("Этот Username занят другим пользователем.")

        if email and CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Этот Email занят другим пользователем.")

        if username == 'me':
            raise serializers.ValidationError("Username 'me' использовать нельзя.")

        return data

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')
