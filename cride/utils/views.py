"""Utils views."""

# DRF
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

# Models
from cride.circles.models import Circle


class AddCicleMixin(viewsets.GenericViewSet):
    """Add circle mixin.

    Manage adding a circle object to views that require it.
    """

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists."""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(AddCicleMixin, self).dispatch(request, *args, **kwargs)
