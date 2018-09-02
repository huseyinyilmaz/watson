# from celery.utils.log import get_task_logger
# from celery import shared_task
from celery.task import task
from logging import getLogger
from screenshots.models import Screenshot
from screenshots.utils import get_driver
from core import constants
from time import sleep
from selenium.common.exceptions import WebDriverException
import hashlib

import base64
import PIL
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

logger = getLogger(__name__)

get_height_script = """
var body = document.body,
    html = document.documentElement;

var height = Math.max(
  body.scrollHeight, body.offsetHeight,
  html.clientHeight, html.scrollHeight, html.offsetHeight );

return height;
"""
# "return document.body.scrollHeight"


def get_height(driver):
    return driver.execute_script(get_height_script)


def set_dimensions(driver, dimension):
    height = -1
    new_height = get_height(driver)
    count = 0
    while height != new_height:
        height, new_height = new_height, get_height(driver)
        driver.set_window_size(dimension.width, height)
        sleep(2)
        count += 1
        if count == 20:
            return


@task(ignore_result=True)
def process_screenshot(screenshot_id):
    screenshot = Screenshot.objects.get(id=screenshot_id)
    dimension = constants.get_dimension(screenshot.dimension)
    browser = constants.get_browser(screenshot.browser)
    try:
        driver = get_driver(browser, dimension)
    except WebDriverException as e:
        logger.exception('There were an error  getting the driver.')
        raise
    try:
        driver.get(screenshot.address)
        driver.set_window_size(dimension.width, dimension.height)
        sleep(screenshot.delay)
        set_dimensions(driver, dimension)
        # get base64 image
        data = driver.get_screenshot_as_base64()
        # turn it into PIL image
        image_data = io.BytesIO(base64.b64decode(data))
        image = PIL.Image.open(image_data)
        # choose 256 colors for png
        image = image.quantize()
        # turn PIL image to binary file
        binary = io.BytesIO()
        image.save(binary, 'png', optimize=True)
        binary.seek(0)
        # get sha1 hash of content:
        h = hashlib.sha1()
        h.update(image_data.read())
        code = h.hexdigest()
        file_name = f'{code}.png'
        f = InMemoryUploadedFile(
            binary,       # file
            None,         # field_name
            file_name,    # file name
            'image/png',  # content_type
            binary.tell,  # size
            None)         # content_type_extra
        # save file to file backend.
        screenshot.image.save(f.name, f)
        screenshot.code = code
        screenshot.save()
        logger.debug('Completed taking screenshot')
    except WebDriverException as e:
        logger.exception("Error in webdriver.")
        driver.quit()
        raise
    except Exception as e:
        driver.quit()
        raise
    driver.quit()
