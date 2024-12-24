from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, TitleSerializer, ReviewSerializer)
from .mixins import ListCreateDestroyViewSet
from reviews.models import Category, Comment, Genre, Review, Title, User


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
        rating=Avg('reviews__score')
    ).order_by('rating')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        serializer.save(
            category=get_object_or_404(
                Category, slug=self.request.data.get('category')
            ),
            genre=Genre.objects.filter(
                slug__in=self.request.data.get('genre', [])
            )
        )

    def perform_update(self, serializer):
        self.perform_create(serializer)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзывов."""
    pass


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев."""
    pass
