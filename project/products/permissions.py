from rest_framework.permissions import BasePermission, SAFE_METHODS

class CustomtPermission(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.user_type == 'admin'
