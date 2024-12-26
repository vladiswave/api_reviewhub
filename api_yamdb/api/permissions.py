from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка на админа или разрешение на чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.role == 'admin')
        )


class IsUserOrAdminOrModeratorOrReadOnly(permissions.BasePermission):
    """Проверка на аутентифицированного пользователя и доп. логику."""

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and (
                request.user == obj.author
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
            )
        )
