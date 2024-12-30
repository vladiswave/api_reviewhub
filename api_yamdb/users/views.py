from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import status

from users.models import CustomUser
from users.permissions import IsAdmin
from users.serializers import UserSerializerForAdmins, UserSerializerForAll
from rest_framework.exceptions import MethodNotAllowed


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет данных пользователей для админа."""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializerForAdmins
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    def get_permissions(self):
        """Возвращает права доступа в зависимости от действия."""
        if self.action == 'me' or self.action == 'update_me':
            return (IsAuthenticated(),)
        return (IsAdmin(),)

    @action(detail=False, methods=['get', 'delete'], url_path='me', url_name='me')
    def me(self, request):
        """Возвращает профиль текущего пользователя."""
        if request.method == 'DELETE':
            raise MethodNotAllowed('DELETE')
        user = self.request.user
        serializer = UserSerializerForAll(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @me.mapping.patch
    def update_me(self, request):
        """Обновляет профиль текущего пользователя."""
        user = self.request.user
        serializer = UserSerializerForAll(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
