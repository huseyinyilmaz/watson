from logging import getLogger

from screenshots.models import ScreenshotSnapshot
from screenshots.utils import get_driver
from core import constants
from core import dsl
from time import sleep
from selenium.common.exceptions import WebDriverException

import dataclasses
import base64
import PIL
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import json
import hashlib

logger = getLogger(__name__)


class Page:
    _get_info_script = """
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

    def __init__(self, screenshot):
        self.screenshot = screenshot
        self.device = constants.get_device(self.screenshot.device)
        try:
            self.driver = get_driver(self.device)
            logger.debug('Driver instance created.')
        except WebDriverException:
            logger.exception('There were an error  getting the driver.')
            raise

    def set_window_size(self, device):
        self._current_device = device
        self.driver.set_window_size(device.width, device.height)

    def scroll_down(self):
        height = self.get_page_height()
        self.driver.execute_script(f'window.scrollBy(0, {height});')

    def load(self):
        """Load the page and wait for screenshot delay."""
        self.driver.get(self.screenshot.url)

    def run_script(self, log_list):
        script = dsl.get_script(self.screenshot.script)
        script(
            driver=self.driver,
            log=log_list.append)
        return logger

    def get_info(self):
        """load page information"""
        info = self.driver.execute_script(self._get_info_script)
        self._info = json.loads(info)
        return self._info

    def get_page_height(self):
        """
        Page height can be get from different attributes for
        different pages.
        We are checking most specific to most general.
        """
        info = self.get_info()
        if info['body']['clientHeight'] > 0:
            return info['body']['clientHeight']
        elif info['html']['clientHeight'] > 0:
            return info['html']['clientHeight']
        else:
            return info['window']['innerHeight']

    def has_scroll(self):
        self.scroll_down()
        info = self.get_info()
        return info['window']['scrollY'] > 0

    def adjust_width(self, result=False):
            new_device = dataclasses.replace(
                self.device,
                width=self.device.selenium_width)
            self.set_window_size(new_device)

    def _adjust_width(self, result=False):
        """If no change is done on page return False else return True """
        logger.debug('Adjusting page width')
        # logger.debug('info = %s', info)
        inner_width = self.get_page_width()
        current_width = self._current_device.width
        target_width = self.device.width
        error_width = target_width - inner_width
        logger.debug('inner_width= %s, current_width= %s, error_width= %s',
                     inner_width,
                     current_width,
                     error_width,
                     )
        if error_width == 0:
            return result
        else:
            new_width = current_width + error_width
            new_device = dataclasses.replace(
                self._current_device,
                width=new_width)
            self.set_window_size(new_device)
            self.adjust_width(True)

    def adjust_height(self, result=False):
        logger.debug('Adjusting page width')
        if self.has_scroll():
            if self._current_device.height == constants.MAXIMUM_SCREENSHOT_HEIGHT: # noqa
                return result
            self.scroll_down()
            info = self.get_info()
            new_height = (self._current_device.height +
                          info['window']['scrollY'])
            new_height = min(new_height, constants.MAXIMUM_SCREENSHOT_HEIGHT)
            # current_height = self._current_device.height
            new_device = dataclasses.replace(
                self._current_device,
                height=new_height)
            logger.debug('Previous dim: %s', self._current_device)
            logger.debug('Current dim: %s', new_device)
            logger.debug('new height: %s', new_height)
            logger.debug('info: %s', self.get_info())
            self.set_window_size(new_device)
            return self.adjust_height(True)
        else:
            return False

    def adjust_dimension(self):
        self.set_window_size(self.device)
        # self.adjust_width()

    def _adjust_dimension(self):
        self.adjust_width()
        self.adjust_height()
        self.adjust_width()
        self.adjust_height()

    def save_screenshot(self):
        self.set_window_size(self.device)
        # TODO remove sleep
        sleep(self.screenshot.delay)
        log_list = []
        self.run_script(log_list)
        # get base64 image
        data = self.driver.get_screenshot_as_base64()
        # import ipdb; ipdb.set_trace()
        # turn it into PIL image
        image_data = io.BytesIO(base64.b64decode(data))
        image = PIL.Image.open(image_data)
        # import ipdb; ipdb.set_trace()

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
        result = {
            'success': True,
            'width': image.width,
            'height': image.height,
            'logs': log_list,
        }
        self.screenshot.image.save(f.name, f)
        self.screenshot.code = code
        self.screenshot.result = json.dumps(result)
        self.screenshot.save()

    def get_page_width(self):
        raise NotImplementedError()


class ChromePage(Page):
    def get_page_width(self):
        info = self.get_info()
        return info['window']['innerWidth']


class FirefoxPage(Page):
    def get_page_width(self):
        info = self.get_info()
        return info['html']['clientWidth']


PAGE_MAP = {
    constants.Backend.FIREFOX: FirefoxPage,
    constants.Backend.CHROME: ChromePage,
}


def get_page(screenshot_id):
    screenshot = ScreenshotSnapshot.objects.get(id=screenshot_id)
    device = constants.get_device(screenshot.device)
    return PAGE_MAP[device.backend](screenshot)
