from rest_framework import serializers
from projects import models


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = '__all__'


class ScreenshotSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Screenshot
        fields = '__all__'
