from rest_framework.permissions import BasePermission


class TaskPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and\
            str(request.user.id) == request.data['user']