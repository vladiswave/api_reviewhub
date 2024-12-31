from django.db.models import Avg, IntegerField
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView


from .filters import TitleFilter
from users.permissions import (IsAdminOrReadOnly,
                               IsUserOrAdminOrModeratorOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, TitleReadSerializer,
                          TitleWriteSerializer, ReviewSerializer)
from .viewsets import ListCreateDestroyViewSet
from .mixins import ListCreateDestroyViewSet
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsUserOrAdminOrModeratorOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    ReviewSerializer,
    UserRegistrationSerializer,
    CustomTokenSerializer,
    UserSerializerForAdmins,
    UserSerializerForAll,
)
from reviews.models import Category, Genre, Review, Title
from users.models import YamdbUser


class CategoriesViewSet(ListCreateDestroyViewSet):
    """Вьюсет категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    """Вьюсет жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет произведений."""

    queryset = Title.objects.annotate(
        rating=Cast(Avg('reviews__score'), IntegerField())
    ).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering_fields = ['name', 'year', 'rating']
    ordering = ['name']
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsUserOrAdminOrModeratorOrReadOnly,
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        return self.get_title().reviews.all()

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsUserOrAdminOrModeratorOrReadOnly,
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        return self.get_review().comments.all()

    def get_review(self):
        return get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id')
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UserRegistrationView(APIView):
    """Вьюсет регистрации пользователей."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Вьюсет выпуска токена."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет данных пользователей."""

    queryset = YamdbUser.objects.all()
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

    @action(detail=False, methods=['get', 'delete'],
            url_path='me', url_name='me')
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
        serializer = UserSerializerForAll(user, data=request.data,
                                          partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
