from rest_framework import viewsets
from rest_framework import mixins

from screenshots import models
from screenshots import serializers


class ScreenshotSnapshotViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.CreateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    """
    Creates new screenshot entry.

    A screenshot will probably take around 10 seconds to complete.
    After screenshot is ready, url will be added to image field on response.
    """
    serializer_class = serializers.ScreenshotSnapshotSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get('organization')
        if organization_id:
            if (self.request.user.organizations
                    .filter(id=organization_id).exists()):
                screenshots = (models.ScreenshotSnapshot.objects
                               .filter(organization=organization_id))
            else:
                # user does not belong to organization
                screenshots = models.ScreenshotSnapshot.objects.none()
        else:
            organization_ids = self.request.user.organizations.values_list(
                'id', flat=True)
            # return screenshots that user can see.
            screenshots = (models.ScreenshotSnapshot.objects
                           .filter(organization__in=organization_ids))

        return screenshots


class ProjectViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    Creates new screenshot entry.

    A screenshot will probably take around 10 seconds to complete.
    After screenshot is ready, url will be added to image field on response.
    """
    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get('organization')
        if organization_id:
            if (self.request.user.organizations
                    .filter(id=organization_id).exists()):
                projects = (models.Project.objects
                            .filter(organization=organization_id))
            else:
                # user does not belong to organization
                projects = models.Project.objects.none()
        else:
            organization_ids = self.request.user.organizations.values_list(
                'id', flat=True)
            # return screenshots that user can see.
            projects = (models.Project.objects
                        .filter(organization__in=organization_ids))

        return projects
