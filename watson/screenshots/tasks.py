# from celery.utils.log import get_task_logger
from celery import shared_task
from logging import getLogger
from screenshots.models import Screenshot

logger = getLogger(__name__)


@shared_task
def process_screenshot(screenshot_id):
    screenshot = Screenshot.objects.get(id=screenshot_id)
    logger.info('Got screenshot %s', screenshot)
    return 1
