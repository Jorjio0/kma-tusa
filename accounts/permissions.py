from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = "Цю дію може виконати лише адміністратор."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
