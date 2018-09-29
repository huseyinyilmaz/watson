from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.conf import settings


# https://chromium.googlesource.com/chromium/src/+/master/chrome/common/chrome_switches.cc
# http://www.assertselenium.com/java/list-of-chrome-driver-command-line-arguments/
def get_driver(dimension):
    options = Options()
    # options.set_headless(True)
    # options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-overlay-scrollbar')
    options.add_argument('--disable-smooth-scrolling')
    options.add_argument('--disable-threaded-scrolling')
    driver = webdriver.Remote(
        command_executor=settings.SELENIUM_COMMAND_EXECUTER,
        desired_capabilities=options.to_capabilities(),
    )
    return driver

    # mobile_emulation = { "deviceName": "Nexus 5" }
    # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
