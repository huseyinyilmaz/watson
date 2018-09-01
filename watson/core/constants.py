from dataclasses import dataclass
from dataclasses import field
from enum import Enum


class Browser(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"


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


dimensions_list = [
    Dimension(code='260X640', name='Galaxy S5', width=260, height=640),
    Dimension(code='768X1024', name='IPad', width=768, height=1024),
    Dimension(code='1024X768', name='Desktop', width=1024, height=768),
    Dimension(code='1440X900', name='Macbook', width=1440, height=900),
]

dim = dimensions_list[0]
# import ipdb; ipdb.set_trace()

dimensions = {dimension.name: dimension
              for dimension in dimensions_list}

DIMENSIONS_CHOICES = [
    (d.name, d) for d in dimensions_list
]

# import ipdb; ipdb.set_trace()

BROWSERS_CHOICES = [
    (b.name, b.name)
    for b in Browser
]
