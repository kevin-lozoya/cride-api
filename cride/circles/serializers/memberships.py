"""Membership serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from cride.circles.models import Membership

# Serializers
from cride.users.serializers.users import UserModelSerializer


class MembershipModelSerializer(serializers.ModelSerializer):
    """Member model serializer."""

    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()
    joined_at = serializers.DateTimeField(source='created', read_only=True)

    class Meta:
        """Meta class."""

        model = Membership
        fields = (
            'user',
            'is_admin', 'is_active',
            'used_invitations', 'remaining_invitations',
            'invited_by',
            'rides_taken', 'rides_offered',
            'joined_at'
        )

        read_only_fields = (
            'user',
            'user_invitations',
            'invited_by',
            'rides_taken', 'rides_offered',
        )