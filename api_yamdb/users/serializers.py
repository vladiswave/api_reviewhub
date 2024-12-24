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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not self.context['request'].user.is_admin:
            representation.pop('role', None)
        return representation

    def validate(self, data):
        current_user_id = self.context['request'].user.id
        username = data.get('username')
        email = data.get('email')

        if username and CustomUser.objects.filter(username=username).exclude(id=current_user_id).exists():
            raise serializers.ValidationError("Этот Username занят другим пользователем.")

        if email and CustomUser.objects.filter(email=email).exclude(id=current_user_id).exists():
            raise serializers.ValidationError("Этот Email занят другим пользователем.")

        if username == 'me':
            raise serializers.ValidationError("Username 'me' использовать нельзя.")

        return data

    class Meta:
        model = CustomUser
        exclude = ('id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'confirmation_code', 'groups', 'user_permissions')
