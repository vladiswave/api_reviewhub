from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CommentViewSet,
                    CustomTokenObtainPairView, GenreViewSet, TitleViewSet,
                    ReviewViewSet, UserRegistrationView, UserViewSet,)


router_version_1 = DefaultRouter()
router_version_1.register(
    r'categories', CategoriesViewSet, basename='categories'
)
router_version_1.register(r'genres', GenreViewSet, basename='genres')
router_version_1.register(r'titles', TitleViewSet, basename='titles')
router_version_1.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_version_1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_version_1.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/', include(router_version_1.urls)),
    path('v1/auth/signup/', UserRegistrationView.as_view(), name='signup'),
    path('v1/auth/token/', CustomTokenObtainPairView.as_view(), name='token'),
]
