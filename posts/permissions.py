from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Только автор может редактировать и удалять, остальные — только чтение."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Администратор имеет полный доступ, остальные — только чтение."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
