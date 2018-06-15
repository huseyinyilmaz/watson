from django.db import models
from accounts.models import Organization
from core import constants
from django_extensions.db.models import TimeStampedModel


class Project(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Screenshot(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    size = models.CharField(max_length=255,
                            choices=constants.SIZE_CHOICES)
    browser = models.CharField(max_length=255,
                               choices=constants.BROWSER_CHOICES)
