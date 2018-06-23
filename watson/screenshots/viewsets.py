from rest_framework import viewsets
from rest_framework import mixins

from screenshots import models
from screenshots import serializers


class ScreenshotViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates new screenshot entry.

    A screenshot will probably take around 10 seconds to complete.
    After screenshot is ready, url will be added to image field on response.
    """
    queryset = models.Screenshot.objects.all()
    serializer_class = serializers.ScreenshotSerializer
