from rest_framework import serializers
from screenshots import models
from screenshots import tasks
from screenshots import constants

from logging import getLogger

logger = getLogger(__name__)


class ScreenshotSerializer(serializers.ModelSerializer):
    """
    ScreenshotSerializer
    """
    organization = serializers.CharField(max_length=255)

    def create(self, validated_data):
        """Create a token for user."""
        user = self.context['request'].user
        import ipdb; ipdb.set_trace()

        object = super().create(validated_data)
        # task = tasks.process_screenshot.delay(object.pk)
        tasks.process_screenshot(object.pk)
        # response = task.get()
        # tasks.process_screenshot(object.pk)
        # logger.info('Task response = %s', response)
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
                  'status', 'image', 'organization']
        read_only_fields = ['id', 'image', 'code', 'result', 'status']
