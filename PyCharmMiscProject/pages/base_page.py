from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config import BASE_TIMEOUT


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, BASE_TIMEOUT)

    def wait_for_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_text_in_element(self, locator, text):
        self.wait.until(EC.text_to_be_present_in_element(locator, text))

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url