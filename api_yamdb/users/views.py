from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer
from .permissions import IsAdmin
from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework.generics import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
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

    # def update(self, request, *args, **kwargs):
    #     raise MethodNotAllowed(method="PUT")


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        allowed_fields = ('username', 'email', 'first_name', 'last_name', 'bio')
        update_data = {key: value for key, value in request.data.items() if key in allowed_fields}
        for field, value in update_data.items():
            setattr(user, field, value)
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
