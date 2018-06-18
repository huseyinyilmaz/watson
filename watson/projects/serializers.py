from rest_framework import serializers
from projects import models
from logging import getLogger


logger = getLogger(__name__)


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = '__all__'
