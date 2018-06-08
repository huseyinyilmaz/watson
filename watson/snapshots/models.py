from django.db import models

from accounts.models import Company


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    company = models.ForeignKey(Company)


class Snapshot(models.Model):
    project = models.ForeignKey(Project)
