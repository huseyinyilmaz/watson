from dataclasses import dataclass
from enum import Enum


class Browser(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"


class Status(Enum):
    PROCESSING = 'processing'
    SUCCESS = 'success'
    FAILURE = 'failure'


@dataclass(frozen=True)
class Dimension:
    name: str
    code: str
    width: int
    height: int


@dataclass(frozen=True)
class Environment:
    '''Class for keeping track of an item in inventory.'''
    dimension: Dimension
    browser: Browser


dimensions_list = [
    Dimension(name='Galaxy S5', code='260x640', width=260, height=640),
    Dimension(name='IPad', code='768x1024', width=768, height=1024),
    Dimension(name='Desktop', code='1024x768', width=1024, height=768),
    Dimension(name='Macbook', code='1440x900', width=1440, height=900),
]


dimensions = {dimension.code: dimension
              for dimension in dimensions_list}

DIMENSIONS_CHOICES = [
    (d.code, str(d))
    for d in dimensions_list
]

STATUS_CHOICES = [
    (s.value, s.name)
    for s in Status
]

BROWSERS_CHOICES = [
    (b.value, b.name)
    for b in Browser
]


def get_dimension(code):
    return dimensions[code]


def get_browser(code):
    return Browser(code)


# BROWSER_CHROME_HEADLESS = 'chrome'
# BROWSER_FIREFOX_HEADLESS = 'ff'

# BROWSER_CHOICES = [
#     (BROWSER_CHROME_HEADLESS, BROWSER_CHROME_HEADLESS),
#     (BROWSER_FIREFOX_HEADLESS, BROWSER_FIREFOX_HEADLESS),
# ]

# SIZE_GALAXY_S5 = '360x640'
# SIZE_IPAD = '768x1024'
# SIZE_MACBOOK = '1440x900'

# SIZE_CHOICES = [
#     ('Galaxy S5 (260x640)', SIZE_GALAXY_S5),
#     ('IPad (768x1024)', SIZE_IPAD),
#     ('Macbook (1440x900)', SIZE_MACBOOK),
# ]
