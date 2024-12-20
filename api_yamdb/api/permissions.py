from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка на админа или разрешение на чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user and request.user.is_staff)
        )
