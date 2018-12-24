from rest_framework import viewsets
from rest_framework import mixins

from screenshots import models
from screenshots import serializers

from screenshots import dsl


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
        project_id = self.request.query_params.get('project')
        if project_id:
            if (self.request.user.organizations
                    .filter(project__id=project_id).exists()):
                screenshots = (models.ScreenshotSnapshot.objects
                               .filter(project=project_id))
            else:
                # user does not belong to organization
                screenshots = models.ScreenshotSnapshot.objects.none()
        else:
            project_ids = self.request.user.organizations.values_list(
                'project__id', flat=True)
            # return screenshots that user can see.
            screenshots = (models.ScreenshotSnapshot.objects
                           .filter(project__in=project_ids))
        script = "'st\\'ring'"
        val = dsl.decode(script)
        print(val)
        import ipdb; ipdb.set_trace()

        return screenshots
