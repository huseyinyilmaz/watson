# from celery.utils.log import get_task_logger
# from celery import shared_task
from celery.task import task
from logging import getLogger
from selenium.common.exceptions import WebDriverException
from screenshots.page import get_page


logger = getLogger(__name__)


@task(ignore_result=True)
def process_screenshot(screenshot_id):
    logger.debug('Starting to take screenshot for %s', screenshot_id)
    page = get_page(screenshot_id)
    try:
        page.load()
        page.adjust_dimension()
        page.save_screenshot()
        logger.debug('Screenshot dimensions after save: %s',
                     page._current_device)
        logger.debug('Info: %s', page.get_info())
    except WebDriverException:
        logger.exception("Error in webdriver.")
        page.driver.quit()
        raise
    except Exception:
        page.driver.quit()
        raise
    page.driver.quit()
