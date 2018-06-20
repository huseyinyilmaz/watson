from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.conf import settings



def get_driver(dimension):
    options = Options()
    options.set_headless(True)
    options.add_argument('--hide-scrollbars')
    # https://peter.sh/experiments/chromium-command-line-switches/
    # options.add_argument('--hide-scrollbars')
    #options.add_argument('--disable-overlay-scrollbar')
    # options.add_argument('--incognito')
    print('XXXXX', options.to_capabilities())
    driver = webdriver.Remote(
        command_executor=settings.SELENIUM_COMMAND_EXECUTER,
        desired_capabilities=options.to_capabilities(),
    )
    return driver
