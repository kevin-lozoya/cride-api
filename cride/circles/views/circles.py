"""Circle views."""

# Django REST Framework
from rest_framework import viewsets

# Models
from cride.circles.models import Circle

# Serializers
from cride.circles.serializers import CircleModelSerializer

class CircleViewSet(viewsets.ModelViewSet):
    """Circle view set."""

    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
