from core import constants

from screenshots import chrome
from screenshots import firefox


get_backend_map = {
    constants.Backend.CHROME: chrome.get_driver,
    constants.Backend.FIREFOX: firefox.get_driver,
}


def get_driver(device):
    if device in get_backend_map:
        return get_backend_map[device](device)
    else:
        return None
