# from celery.utils.log import get_task_logger
from django.core.files.uploadedfile import InMemoryUploadedFile
from celery import shared_task
from logging import getLogger
from screenshots.models import Screenshot
from screenshots.utils import get_driver
from screenshots import constants
import base64
import PIL
import io
import datetime


logger = getLogger(__name__)


@shared_task
def process_screenshot(screenshot_id):
    screenshot = Screenshot.objects.get(id=screenshot_id)
    dimension = constants.get_dimension(screenshot.dimension)
    driver = get_driver(constants.get_browser(screenshot.browser), dimension)
    driver.get(screenshot.url)
    height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(dimension.width, height)
    body = driver.find_element_by_tag_name('body')
    data = driver.get_screenshot_as_base64()
    image_data = io.BytesIO(base64.b64decode(data))
    image = PIL.Image.open(image_data)
    image = image.convert('RGB')
    binary = io.BytesIO()
    image.save(binary, 'jpeg', optimize=True)
    binary.seek(0)
    img_name = str(datetime.datetime.now()) + '.jpeg'
    screenshot.image.save(
        img_name,
        InMemoryUploadedFile(
            binary,       # file
            None,         # field_name
            img_name,     # file name
            'image/jpeg', # content_type
            image.tell,   # size
            None),        # content_type_extra
    )
    screenshot.save()
    logger.info('Got screenshot %s', screenshot)
    logger.info('Got driver %s', driver)
    driver.close()
    return 1
