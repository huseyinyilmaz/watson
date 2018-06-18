from django.db import models
from environments import constants
from django_extensions.db.models import TimeStampedModel


class Screenshot(TimeStampedModel):
    url = models.URLField()
    dimension = models.CharField(max_length=255,
                                 choices=constants.DIMENSIONS_CHOICES)
    browser = models.CharField(max_length=255,
                               choices=constants.BROWSERS_CHOICES)
    image = models.ImageField(blank=True,
                              upload_to='media/projects-screenshot-image')
