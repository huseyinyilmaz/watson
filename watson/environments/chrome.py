from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

WINDOW_SIZE = "1920,1080"

driver = webdriver.Remote(
    command_executor='http://selenium:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME)

driver.set_window_size(1920, 1080)
