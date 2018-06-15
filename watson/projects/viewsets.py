from rest_framework import viewsets
from rest_framework import mixins

from projects import models
from projects import serializers


class ProjectViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer


class ScreenshotViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    queryset = models.Screenshot.objects.all()
    serializer_class = serializers.ScreenshotSerializer
