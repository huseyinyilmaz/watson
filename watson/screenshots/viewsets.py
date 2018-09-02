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
    serializer_class = serializers.ScreenshotSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get('organization')
        if organization_id:
            if (self.request.user.organizations
                    .filter(id=organization_id).exists()):
                screenshots = (models.Screenshot.objects
                               .filter(organization__id=organization_id))
            else:
                # user does not belong to organization
                screenshots = models.Screenshot.objects.none()
        else:
            # return screenshots that user can see.
            screenshots = (models.Screenshot.objects
                           .filter(organization__user=self.request.user))

        return screenshots
