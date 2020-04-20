from django.utils.translation import gettext as _
from rest_framework.permissions import BasePermission


class IsVerified(BasePermission):
    """
    Allows access only to verified users.
    """
    message = _("User was not verified")

    def has_permission(self, request, view):
        return request.user and request.user.is_verified
