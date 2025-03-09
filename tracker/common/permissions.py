from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsAdmin(BasePermission):
    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role != "admin":
            raise PermissionDenied(
                "You do not have permission to access this resource."
            )

        return True
