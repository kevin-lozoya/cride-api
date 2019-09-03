"""Rides views."""

# DRF
from rest_framework import mixins

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember

# Serializers
from cride.rides.serializers import CreateRideSerializer

# Utilities
from cride.utils.views import AddCicleMixin


class RideViewSet(mixins.CreateModelMixin,
                  AddCicleMixin):
    """Ride view set."""

    serializer_class = CreateRideSerializer
    permission_classes = [IsAuthenticated, IsActiveCircleMember]

    def get_serializer_context(self):
        """Add circle to serializer context."""
        context = super(RideViewSet, self).get_serializer_context()
        context['circle'] = self.circle
        return context
