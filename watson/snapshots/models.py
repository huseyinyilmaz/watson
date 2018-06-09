from django.db import models

from accounts.models import Company


class Setup(models.Model):

    """Test setup."""

    width = models.NumberField()
    height = models.NumberField()
    browser = models.CharField(max_length=255)


class Project(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    company = models.ForeignKey(Company)


class Snapshot(models.Model):
    project = models.ForeignKey(Project)
    setup = models.ForeignKey(Setup)
