from django.db import models
from accounts.models import Organization


class Project(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'
