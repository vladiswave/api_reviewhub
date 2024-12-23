from rest_framework import permissions


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'user'


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'moderator'


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser
