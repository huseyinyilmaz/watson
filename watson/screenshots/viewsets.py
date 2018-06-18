from rest_framework import viewsets
from rest_framework import mixins

from screenshots import models
from screenshots import serializers


class ScreenshotViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    queryset = models.Screenshot.objects.all()
    serializer_class = serializers.ScreenshotSerializer
