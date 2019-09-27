"""Rides views."""

from datetime import timedelta

# Django
from django.utils import timezone

# DRF
from rest_framework import mixins

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember
from cride.rides.permissions.rides import IsRideOwner

# Serializers
from cride.rides.serializers import CreateRideSerializer, RideModelSerializer

# Utilities
from cride.utils.views import AddCicleMixin


class RideViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  AddCicleMixin):
    """Ride view set."""

    serializer_class = CreateRideSerializer
    permission_classes = [IsAuthenticated, IsActiveCircleMember]
    filter_backends = [SearchFilter, OrderingFilter]
    ordering = ['departure_date', 'arrival_date', 'available_seats']
    ordering_fields = ['departure_date', 'arrival_date', 'available_seats']
    search_fields = ['departure_location', 'arrival_location']

    def get_permissions(self):
        """Assign permission based on action."""
        permissions = [IsAuthenticated, IsActiveCircleMember]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsRideOwner)
        return [p() for p in permissions]

    def get_serializer_context(self):
        """Add circle to serializer context."""
        context = super(RideViewSet, self).get_serializer_context()
        context['circle'] = self.circle
        return context

    def get_serializer_class(self):
        """Return serialzier based on action."""
        if self.action == 'create':
            return CreateRideSerializer
        return RideModelSerializer

    def get_queryset(self):
        """Return active circle's rides."""
        offset = timezone.now() + timedelta(minutes=10)
        return self.circle.ride_set.filter(
            departure_date__gte=offset,
            is_active=True,
            available_seats__gte=1
        )
