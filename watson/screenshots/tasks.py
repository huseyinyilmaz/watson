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
from time import sleep



logger = getLogger(__name__)


@shared_task(ignore_result=True)
def process_screenshot(screenshot_id):
    screenshot = Screenshot.objects.get(id=screenshot_id)
    dimension = constants.get_dimension(screenshot.dimension)
    browser = constants.get_browser(screenshot.browser)
    driver = get_driver(browser, dimension)

    try:
      driver.get(screenshot.url)
      sleep(3)
      height = driver.execute_script("return document.body.scrollHeight")
      driver.set_window_size(dimension.width, height)
      sleep(3)
      data = driver.get_screenshot_as_base64()
      image_data = io.BytesIO(base64.b64decode(data))
      image = PIL.Image.open(image_data)
      image = image.convert('RGB')
      binary = io.BytesIO()
      image.save(binary, 'jpeg', optimize=True)
      binary.seek(0)
      img_name = f'{browser.value}-{dimension}-{datetime.datetime.now()}.jpeg'
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
    except Exception as e:
        print(e)
    else:
      driver.quit()


    return 1
