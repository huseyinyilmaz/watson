import base64
import PIL
import io
import datetime
from django.core.files.uploadedfile import InMemoryUploadedFile

from screenshots import chrome
from screenshots import firefox
from screenshots import constants


get_driver_map = {
    constants.Browser.CHROME: chrome.get_driver,
    constants.Browser.FIREFOX: firefox.get_driver,
}


def get_driver(browser, dimension):
    if browser in get_driver_map:
        return get_driver_map[browser](dimension)
    else:
        return None


def get_screenshot(driver):
    data = driver.get_screenshot_as_base64()
    image_data = io.BytesIO(base64.b64decode(data))
    image = PIL.Image.open(image_data)
    # choose 256 colors for png
    image = image.quantize()
    binary = io.BytesIO()
    image.save(binary, 'png', optimize=True)
    binary.seek(0)
    img_name = f'{datetime.datetime.now()}.png'
    return InMemoryUploadedFile(
        binary,        # file
        None,          # field_name
        img_name,      # file name
        'image/png',  # content_type
        image.tell,    # size
        None),         # content_type_extra
