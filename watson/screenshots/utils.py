from core import constants

from screenshots import chrome
from screenshots import firefox


get_driver_map = {
    constants.Browser.CHROME: chrome.get_driver,
    constants.Browser.FIREFOX: firefox.get_driver,
}


def get_driver(browser, dimension):
    if browser in get_driver_map:
        return get_driver_map[browser](dimension)
    else:
        return None
