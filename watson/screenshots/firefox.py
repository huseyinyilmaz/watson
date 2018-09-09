from selenium import webdriver

# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.conf import settings

# http://kb.mozillazine.org/About:config_entries
# http://kb.mozillazine.org/Category:Preferences


def get_driver(dimension):
    fp = FirefoxProfile()
    # fp.set_preference('media.navigator.permission.disabled', True)
    fp.update_preferences()
    caps = DesiredCapabilities.FIREFOX.copy()
    caps['firefox_profile'] = fp.encoded
    # caps['marionette'] = True
    # webdriver.Firefox(capabilities=caps)

    # options = Options()
    # options.set_headless(True)
    # options.add_argument('--hide-scrollbars')
    # caps = options.to_capabilities()
    driver = webdriver.Remote(
        command_executor=settings.SELENIUM_COMMAND_EXECUTER,
        desired_capabilities=caps,
    )
    return driver
