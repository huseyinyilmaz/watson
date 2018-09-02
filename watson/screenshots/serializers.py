from rest_framework import serializers
from screenshots import models
from screenshots import tasks
from core import constants

from logging import getLogger

logger = getLogger(__name__)


class ScreenshotSerializer(serializers.ModelSerializer):
    """
    ScreenshotSerializer
    """
    organization = serializers.CharField(max_length=255, write_only=True)

    def create(self, validated_data):
        """Create a token for user."""
        request = self.context['request']
        organization_id = request.data['organization']
        organization = (request.user.organizations
                        .filter(id=organization_id).first())
        if not organization:
            raise serializers.ValidationError(
                {'non_field_errors':
                 ['User is not belong to '
                  f'organization with id { organization_id }']})
        object = super().create(validated_data)
        organization.screenshots.add(object)
        # tasks.process_screenshot.delay(object.pk)
        tasks.process_screenshot(object.pk)
        return object

    class Meta:
        model = models.Screenshot
        extra_kwargs = {
            'status': {
                'default': constants.Status.PROCESSING.value,
                'initial': constants.Status.SUCCESS.value,
            }, 'delay': {'default': 3, 'initial': 3},
        }

        fields = ['id', 'address', 'delay', 'dimension', 'browser',
                  'status', 'result', 'image', 'organization', 'created',
                  'modified']

        write_only_fields = ['organization']
        read_only_fields = ['id', 'image', 'code', 'result', 'status',
                            'result', 'created', 'modified']
