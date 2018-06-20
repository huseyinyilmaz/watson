from rest_framework import serializers
from screenshots import models
from screenshots import tasks
from logging import getLogger

logger = getLogger(__name__)


class ScreenshotSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        """Create a token for user."""
        object = super().create(validated_data)
        task = tasks.process_screenshot.delay(object.pk)
        # response = task.get()
        # tasks.process_screenshot(object.pk)
        # logger.info('Task response = %s', response)
        return object

    class Meta:
        model = models.Screenshot
        read_only_fields = ['image']
        fields = '__all__'
