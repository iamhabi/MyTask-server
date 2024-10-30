from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        elif request.method in ['PUT', 'DELETE']:
            return request.user.is_authenticated
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.method in ['PUT', 'DELETE']:
            return obj == request.user
        else:
            return False