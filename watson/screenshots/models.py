from django.db import models
from screenshots import constants
from django_extensions.db.models import TimeStampedModel
from accounts.models import Organization


class Screenshot(TimeStampedModel):
    # organization screenshot is connected to.
    organization = models.ForeignKey(Organization,
                                     on_delete=models.CASCADE,)
    # Screenshot url
    url = models.URLField()
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
    code = models.CharField(max_length=255)
    # status of screenshot
    status = models.CharField(max_length=255,
                              choices=constants.STATUS_CHOICES)
    # result/error explanation
    result = models.TextField()
    # Result screenshot
    image = models.ImageField(
        blank=True,
        upload_to='media/projects-screenshot-image')
