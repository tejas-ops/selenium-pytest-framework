import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config import BASE_TIMEOUT

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, BASE_TIMEOUT)

    def wait_for_element(self, locator):
        logger.debug("Waiting for element: %s", locator)
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_clickable(self, locator):
        logger.debug("Waiting for clickable: %s", locator)
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_text_in_element(self, locator, text):
        logger.debug("Waiting for text '%s' in element: %s", text, locator)
        self.wait.until(EC.text_to_be_present_in_element(locator, text))

    def get_title(self):
        title = self.driver.title
        logger.debug("Page title: %s", title)
        return title

    def get_current_url(self):
        url = self.driver.current_url
        logger.debug("Current URL: %s", url)
        return url
