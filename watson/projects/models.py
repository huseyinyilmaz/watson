from django.db import models
from accounts.models import Company
from core import constants


class Project(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    company = models.ForeignKey(Company)


class Screenshot(models.Model):
    project = models.ForeignKey(Project)
    size = models.CharField(max_length=255,
                            choices=constants.SIZE_CHOICES)
    browser = models.CharField(max_length=255,
                               choices=constants.BROWSER_CHOICES)
