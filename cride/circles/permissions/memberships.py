"""Circles permission classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership


class IsActiveCircleMember(BasePermission):
    """Allow access only to circle members.

    Expect that the views implementing this permission
    have a 'circle' attribute assigned.
    """

    def has_permission(self, request, view):
        """Vefir user si a n active member of the circle."""
        
        try:
            Membership.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except Membership.DoesNotExiste:
            return False
        return True