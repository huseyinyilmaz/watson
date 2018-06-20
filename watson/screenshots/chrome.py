from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.conf import settings



def get_driver(dimension):
    options = Options()
    # options.set_headless(True)
    options.add_argument('--hide-scrollbars')
    driver = webdriver.Remote(
        command_executor=settings.SELENIUM_COMMAND_EXECUTER,
        desired_capabilities=options.to_capabilities(),
    )
    return driver
