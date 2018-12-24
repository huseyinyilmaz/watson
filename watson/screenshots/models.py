import uuid

from django.db import models

from django_extensions.db.models import TimeStampedModel

from core import constants
from accounts.models import Project

#####################
# Screenshot Models #
#####################


class PageBase(TimeStampedModel):
    # Screenshot url
    url = models.URLField()

    class Meta:
        abstract = True


class Page(PageBase):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class ScreenshotBase(PageBase):
    # Delay after page load.
    delay = models.SmallIntegerField()
    # device
    device = models.CharField(
        max_length=255,
        choices=constants.DEVICE_CHOICES)

    script = models.TextField(blank=True)

    class Meta:
        abstract = True


class Screenshot(ScreenshotBase):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)


#####################
# Snapshot Models #
#####################

class PageSnapshot(PageBase):
    page = models.CharField(max_length=255)
    project = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['page']),
            models.Index(fields=['project']),
        ]


class ScreenshotSnapshot(ScreenshotBase):
    # url => from PageBase
    # delay => from ScreenshotBase
    # dimension => from ScreenshotBase
    # browser => from ScreenshotBase
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # project this screenshot belongs to
    project = models.CharField(max_length=255)
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
    screenshot = models.CharField(max_length=255, blank=True, null=False)
    pagesnapshot = models.ForeignKey(PageSnapshot,
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['screenshot']),
            models.Index(fields=['project']),
        ]
