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
    def create(self, validated_data):
        """Create a token for user."""
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
                  'status', 'organization', 'image']
        read_only_fields = ['id', 'image', 'code', 'result']
