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
import json
from screenshots.page import get_page


logger = getLogger(__name__)

get_info_script = """
var body = document.body,
    html = document.documentElement;

var bodyObj = { scrollHeight: body.scrollHeight,
                scrollWidth: body.scrollWidth,
                offsetHeight: body.offsetHeight,
                offsetWidth: body.offsetWidth,
                clientHeight: body.clientHeight,
                clientWidth: body.clientWidth,
               }

var htmlObj = { scrollHeight: html.scrollHeight,
                scrollWidth: html.scrollWidth,
                offsetHeight: html.offsetHeight,
                offsetWidth: html.offsetWidth,
                innerHeight: html.innerHeight,
                innerWidth: html.innerWidth,
                clientHeight: html.clientHeight,
                clientWidth: html.clientWidth,
               }

var windowObj = { innerHeight: window.innerHeight,
                  innerWidth: window.innerWidth,
                  outerHeight: window.outerHeight,
                  outerWidth: window.outerWidth,
                  scrollY: window.scrollY,
                  scrollX: window.scrollX,
                  }
return JSON.stringify({
    body: bodyObj,
    html: htmlObj,
    window: windowObj,
    });
"""

get_height_script = """
var body = document.body,
    html = document.documentElement;

var height = Math.max(
  body.scrollHeight, body.offsetHeight,
  html.clientHeight, html.scrollHeight, html.offsetHeight );

return height;
"""

get_height_script = """
var body = document.body,
    html = document.documentElement;
return (body.scrollHeight || html.scrollHeight);
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


def get_info(driver):
    info = driver.execute_script(get_info_script)
    return json.loads(info)


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
    # driver.set_window_size(dimension.width, height)
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
    return current_width


def set_height(driver, dimension):
    height = get_height(driver)
    driver.set_window_size(dimension.width, height)
    return height


def set_dimensions(driver, dimension):
    height = constants.MAXIMUM_SCREENSHOT_HEIGHT
    driver.set_window_size(dimension.width, height)
    width = set_width(driver, dimension)
    dimension = dataclasses.replace(dimension, width=width)
    height = set_height(driver, dimension)
    dimension = dataclasses.replace(dimension, height=height)
    reset_scroll(driver)
    return dimension


@task(ignore_result=True)
def process_screenshot(screenshot_id):
    logger.debug('Starting to take screenshot for %s', screenshot_id)
    page = get_page(screenshot_id)
    try:
        page.load()
        page.adjust_dimension()
        page.save_screenshot()
        logger.debug('Screenshot dimensions after save: %s',
                     page._current_device)
        logger.debug('Info: %s', page.get_info())
    except WebDriverException as e:
        logger.exception("Error in webdriver.")
        page.driver.quit()
        raise
    except Exception as e:
        page.driver.quit()
        raise
    page.driver.quit()
