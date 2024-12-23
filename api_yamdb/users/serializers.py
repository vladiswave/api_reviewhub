from rest_framework import serializers
from .models import CustomUser
from django.core.validators import RegexValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, allow_blank=False,)
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message="Username can only contain letters, digits, and @/./+/-/_ characters."
            )
        ]
    )
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username is already taken.")

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is already in use.")

        if username == 'me':
            raise serializers.ValidationError("Username 'me' is not allowed.")

        return data

    class Meta:
        model = CustomUser
        exclude = ('id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'confirmation_code', 'groups', 'user_permissions')
