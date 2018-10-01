from django.db import models
from core import constants
from django_extensions.db.models import TimeStampedModel
import uuid


#####################
# Screenshot Models #
#####################
class Project(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True, unique=True)


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

    class Meta:
        abstract = True


class Screenshot(ScreenshotBase):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)


#####################
# Snapshot Models #
#####################
class ProjectSnapshot(TimeStampedModel):
    project = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['organization']),
        ]


class PageSnapshot(PageBase):
    projectsnapshot = models.ForeignKey(ProjectSnapshot,
                                        on_delete=models.CASCADE)
    page = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['page']),
            models.Index(fields=['organization']),
        ]


class ScreenshotSnapshot(ScreenshotBase):
    # url => from PageBase
    # delay => from ScreenshotBase
    # dimension => from ScreenshotBase
    # browser => from ScreenshotBase
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # organization this screenshot belongs to
    organization = models.CharField(max_length=255)
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
                                     blank=True, null=False)

    class Meta:
        indexes = [
            models.Index(fields=['screenshot']),
            models.Index(fields=['organization']),
        ]
