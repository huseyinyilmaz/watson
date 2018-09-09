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
import dataclasses

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

_get_height_script = """
return html.clientHeight;
"""

get_scroll_y_script = """
return window.scrollY;
"""

scroll_down_script = """
window.scrollBy(0, 10000);
"""

reset_scroll_script = """
window.scrollBy(0, -1000000);
"""
get_width_script = """
return document.body.clientWidth;
// return window.innerWidth;
"""


def get_scroll_y(driver):
    logger.debug('get_scroll_y')
    return driver.execute_script(get_scroll_y_script)


def scroll_down(driver):
    logger.debug('scroll_down')
    return driver.execute_script(scroll_down_script)


def reset_scroll(driver):
    logger.debug('scroll_down')
    return driver.execute_script(reset_scroll_script)


def get_height(driver):
    logger.debug('get_height')
    return driver.execute_script(get_height_script)


def get_width(driver):
    logger.debug('get_width')
    return driver.execute_script(get_width_script)


def set_width(driver, dimension):
    # Use maximum screenshot_height that way we will make sure end result will
    # be using right browser width.
    # (height change will not effect the result width)
    height = constants.MAXIMUM_SCREENSHOT_HEIGHT
    driver.set_window_size(dimension.width, height)
    logger.debug('set_width')
    inner_width = get_width(driver)
    target_width = dimension.width
    current_width = dimension.width
    logger.debug('inner_width %s', inner_width)
    logger.debug('target_width %s', target_width)
    logger.debug('current_width %s', current_width)
    while inner_width < target_width:
        current_width = current_width + (target_width - inner_width)
        driver.set_window_size(current_width, height)
        logger.debug('Page width resized: %s', current_width)
        inner_width = get_width(driver)
    driver.set_window_size(current_width, dimension.height)
    return current_width


def set_height(driver, dimension):
    height = get_height(driver)
    sleep(2)
    new_height = get_height(driver)
    # make sure page size is not expending with new loads.
    count = 0
    while height != new_height:
        sleep(2)
        height, new_height = new_height, get_height(driver)
        driver.set_window_size(dimension.width, height)
        logger.debug('page resized.')
        count += 1
        if count == 10:
            return height
    logger.debug('Page is not getting larger anymore.')
    # make page longer until there is no scroll bar.
    scroll_down(driver)
    current_y = get_scroll_y(driver)
    while current_y > 0:
        height = height + current_y
        height = min(height, constants.MAXIMUM_SCREENSHOT_HEIGHT)
        logger.debug('Page height resized')
        driver.set_window_size(dimension.width, height)
        if height == constants.MAXIMUM_SCREENSHOT_HEIGHT:
            return height
        scroll_down(driver)
        current_y = get_scroll_y(driver)
    return height


def set_dimensions(driver, dimension):
    width = set_width(driver, dimension)
    dimension = dataclasses.replace(dimension, width=width)
    height = set_height(driver, dimension)
    dimension = dataclasses.replace(dimension, height=height)
    reset_scroll(driver)
    sleep(1)
    return dimension


@task(ignore_result=True)
def process_screenshot(screenshot_id):
    logger.debug('Starting to take screenshot for %s', screenshot_id)
    screenshot = Screenshot.objects.get(id=screenshot_id)
    dimension = constants.get_dimension(screenshot.dimension)
    browser = constants.get_browser(screenshot.browser)
    try:
        driver = get_driver(browser, dimension)
        logger.debug('Driver instance created.')
    except WebDriverException as e:
        logger.exception('There were an error  getting the driver.')
        raise
    try:
        driver.get(screenshot.address)
        driver.set_window_size(dimension.width, dimension.height)
        sleep(screenshot.delay)
        logger.debug('Browser initialized.')
        dims = set_dimensions(driver, dimension)
        import ipdb; ipdb.set_trace()

        logger.debug('Ready to take screenshots')
        logger.debug('-' * 80)
        logger.debug('height: %s', get_height(driver))
        logger.debug('width: %s', get_width(driver))
        logger.debug('scroll_y: %s', get_scroll_y(driver))
        logger.debug('-' * 80)
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
