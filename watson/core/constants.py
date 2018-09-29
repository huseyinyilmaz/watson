from dataclasses import dataclass
from dataclasses import field
from enum import Enum

@dataclass(frozen=True)
class Device:
    code: str
    name: str
    width: int
    height: int

device_list = [
    Device(code='desktop_chrome_1440_900',
           name='Desktop Chrome',
           width= 1440, height=900),
    Device(code='desktop_firefox_1440_900',
           name='Desktop Firefox',
           width= 1440, height=900),
    Device(code='ipad',
           name='Ipad',
           width= 768, height=1024),
    Device(code='iphone_x',
           name='Iphone X',
           width= 374, height=812),
    Device(code='pixel_2',
           name='Pixel 2',
           width= 411, height=713),
]

devices = { d.code: d for d in device_list}

DEVICE_CHOICES = [(d.code, str(d)) for d in device_list]

def get_device(code):
    return dimensions[code]

class Browser(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"

class Status(Enum):
    PROCESSING = 'processing'
    SUCCESS = 'success'
    FAILURE = 'failure'


@dataclass(frozen=True)
class Dimension:
    code: str
    name: str
    width: int
    height: int

@dataclass(frozen=True)
class Environment:
    '''Class for keeping track of an item in inventory.'''
    dimension: Dimension
    browser: Browser


MAXIMUM_SCREENSHOT_HEIGHT = 10000


dimensions_list = [
    Dimension(code='260X640', name='Galaxy S5', width=260, height=640),
    Dimension(code='768X1024', name='IPad', width=768, height=1024),
    Dimension(code='1024X768', name='Desktop', width=1024, height=768),
    Dimension(code='1440X900', name='Macbook', width=1440, height=900),
]

dimensions = {dimension.code: dimension
              for dimension in dimensions_list}

DIMENSIONS_CHOICES = [
    (d.code, str(d)) for d in dimensions_list
]

BROWSERS_CHOICES = [
    (b.value, b.name)
    for b in Browser
]

STATUS_CHOICES = [
    (s.value, s.name)
    for s in Status
]


def get_dimension(code):
    return dimensions[code]


def get_browser(code):
    return Browser(code)
