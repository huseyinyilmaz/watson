from dataclasses import dataclass
from enum import Enum


class Browser(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"


@dataclass(frozen=True)
class Dimension:
    name: str
    width: int
    height: int


@dataclass(frozen=True)
class Environment:
    '''Class for keeping track of an item in inventory.'''
    dimension: Dimension
    browser: Browser


dimensions_list = [
    Dimension(name='Galaxy S5', width=260, height=640),
    Dimension(name='IPad', width=768, height=1024),
    Dimension(name='Desktop', width=1024, height=768),
    Dimension(name='Macbook', width=1440, height=900),
]


dimensions = {dimension.name: dimension
              for dimension in dimensions_list}

DIMENSIONS_CHOICES = [
    (dimensions.name, dimensions)
    for d in dimensions_list
]

BROWSERS_CHOICES = [
    (Browser[b], Browser[b])
    for b in Browser
]
