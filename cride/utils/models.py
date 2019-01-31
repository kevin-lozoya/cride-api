from django.db import models

class CRideModel(models.Model):
    """Comparte Ride base model.

    CRideModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Store the datetime the objects was created
        + modified (DateTime): Store the last datetime the objects was modified
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add = True,
        help_text='Date time on which the object was created.'
    )
    modified = models.DateTimeField(
        'modified at',
        autho_now = True,
        help_text='Date time on which the object was modified'
    )

    class Meta:
        """Meta option."""

        abstract = True

        get_lasted_by = 'created'
        ordering = ['-created', '-modified']