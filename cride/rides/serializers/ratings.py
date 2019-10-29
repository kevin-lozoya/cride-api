"""Ratings serializers."""

# Django
from django.db.models import Avg

# DRF
from rest_framework import serializers

# Models
from cride.rides.models import Rating


class CreateRideRatingSerializer(serializers.ModelSerializer):
    """Create ride rating serializer."""

    rating = serializers.IntegerField(min_value=1, max_value=5)
    comments = serializers.CharField(required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        """Meta class."""

        model = Rating
        fields = ['rating', 'comments']

    def validate_user(self, value):
        """Verify user was a passenger."""
        ride = self.context['ride']
        if not ride.passengers.filter(pk=value.pk).exists():
            raise serializers.ValidationError('User is not a passenger')
        return value

    def validate(self, data):
        """Verify rating hasn't been emitted before."""

        q = Rating.objects.filter(
            circle=self.context['circle'],
            ride=self.context['ride'],
            rating_user=data['user'],
        )
        if q.exists():
            raise serializers.ValidationError('Rating have already been emitted!')
        return data

    def create(self, data):
        """Create rating."""
        offered_by = self.context['ride'].offered_by

        Rating.objects.create(
            circle=self.context['circle'],
            ride=self.context['ride'],
            rating_user=data.pop('user'),
            rated_user=offered_by,
            **data
        )

        ride_avg = round(
            Rating.objects.filter(
                circle=self.context['circle'],
                ride=self.context['ride']
            ).aggregate(Avg('rating'))['rating__avg'],
        )
        self.context['ride'].rating = ride_avg
        self.context['ride'].save()

        user_avg = round(
            Rating.objects.filter(
                rated_user=offered_by
            ).aggregate(Avg('rating'))['rating__avg']
        )
        offered_by.profile.reputation = user_avg
        offered_by.profile.save()
        return self.context['ride']