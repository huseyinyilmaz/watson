from django.db import models
from screenshots import constants
from django_extensions.db.models import TimeStampedModel


class Screenshot(TimeStampedModel):
    # Screenshot url
    address = models.URLField()
    # Delay after page load.
    delay = models.SmallIntegerField()
    # Page dimensions.
    dimension = models.CharField(
        max_length=255,
        choices=constants.DIMENSIONS_CHOICES)
    # Browser used for screenshot
    browser = models.CharField(
        max_length=255,
        choices=constants.BROWSERS_CHOICES)
    # content hash of screenshot.
    code = models.CharField(max_length=255, blank=True)
    # status of screenshot
    status = models.CharField(max_length=255,
                              choices=constants.STATUS_CHOICES)
    # result/error explanation
    result = models.TextField(blank=True)
    # image file url.
    image = models.ImageField(
        blank=True,
        upload_to='media/projects-screenshot-image')
