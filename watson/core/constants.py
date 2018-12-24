from dataclasses import dataclass
# from dataclasses import field
from enum import Enum


class Backend(Enum):
    CHROME = 'chrome'
    FIREFOX = 'firefox'


@dataclass(frozen=True)
class Device:
    code: str
    name: str
    width: int
    height: int
    backend: Backend


device_list = [
    Device(code='desktop_chrome_1440_900',
           name='Desktop Chrome',
           width=1440, height=900,
           backend=Backend.CHROME),
    Device(code='desktop_firefox_1440_900',
           name='Desktop Firefox',
           width=1440, height=900,
           backend=Backend.FIREFOX),
    Device(code='ipad',
           name='Ipad',
           width=768, height=1024,
           backend=Backend.CHROME),
    Device(code='iphone_x',
           name='Iphone X',
           width=374, height=812,
           backend=Backend.CHROME),
    Device(code='pixel_2',
           name='Pixel 2',
           width=411, height=713,
           backend=Backend.CHROME),
]

devices = {d.code: d for d in device_list}

DEVICE_CHOICES = [(d.code, str(d)) for d in device_list]


def get_device(code):
    return devices[code]


class Status(Enum):
    PROCESSING = 'processing'
    SUCCESS = 'success'
    FAILURE = 'failure'


MAXIMUM_SCREENSHOT_HEIGHT = 10000


STATUS_CHOICES = [
    (s.value, s.name)
    for s in Status
]
