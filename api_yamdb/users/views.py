from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser
from users.permissions import IsAdmin
from users.serializers import UserSerializerForAdmins, UserSerializerForAll


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет данных пользователей для админа."""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializerForAdmins
    permission_classes = (IsAuthenticated, IsAdmin,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'


class UserProfileViewSet(viewsets.ModelViewSet):
    """Вьюсет профиля пользователя c расширенным доступом."""

    serializer_class = UserSerializerForAll
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'patch',)

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.request.user.id)
