from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializerForAdmins, UserSerializerForAll
from .permissions import IsAdmin
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializerForAdmins
    permission_classes = (IsAuthenticated, IsAdmin,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    def perform_create(self, serializer):
        user = serializer.save()
        return user

    def retrieve(self, request, username=None):
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise NotFound()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializerForAll
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.request.user.id)
