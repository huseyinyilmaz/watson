from rest_framework import serializers
from screenshots import models
from screenshots import tasks
from core import constants
from core import dsl
from logging import getLogger

logger = getLogger(__name__)


class ScreenshotSnapshotSerializer(serializers.ModelSerializer):
    """
    ScreenshotSerializer
    """
    # project = serializers.CharField(max_length=255, write_only=True)

    def validate_script(self, data):
        try:
            dsl.get_script(data)
        except dsl.DSLException as e:
            raise serializers.ValidationError(*e.args)
        return data

    def create(self, validated_data):
        """Create a token for user."""
        request = self.context['request']
        project_id = request.data['project']
        project_exists = (request.user.organizations
                          .filter(project__id=project_id).exists())
        if not project_exists:
            raise serializers.ValidationError(
                {'non_field_errors':
                 ['User is not belong to '
                  f'project with id { project_id }']})

        object = super().create(validated_data)
        # organization.screenshots.add(object)
        # tasks.process_screenshot.delay(object.pk)
        tasks.process_screenshot(object.pk)
        return object

    class Meta:
        model = models.ScreenshotSnapshot
        extra_kwargs = {
            'status': {
                'default': constants.Status.PROCESSING.value,
                'initial': constants.Status.SUCCESS.value,
            }, 'delay': {'default': 3, 'initial': 3},
        }

        fields = ['id', 'code', 'url', 'delay', 'device',
                  'status', 'result', 'image', 'project', 'created',
                  'modified', 'screenshot', 'pagesnapshot', 'script']

        write_only_fields = ['project']
        read_only_fields = ['id', 'code', 'image', 'code', 'result', 'status',
                            'result', 'created', 'modified']
