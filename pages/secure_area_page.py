from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class SecureAreaPage(BasePage):
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a.button.secondary.radius")
    FLASH_MESSAGE = (By.ID, "flash")
    LOGIN_USERNAME = (By.ID, "username")

    def wait_until_loaded(self):
        self.wait_for_clickable(self.LOGOUT_BUTTON)
        self.wait_for_text_in_element(self.FLASH_MESSAGE, "You logged into a secure area!")

    def click_logout(self):
        self.wait_for_clickable(self.LOGOUT_BUTTON).click()
        self.wait_for_text_in_element(self.FLASH_MESSAGE, "You logged out of the secure area!")
        try:
            self.wait.until(EC.url_contains("/login"))
        except TimeoutException:
            self.wait_for_element(self.LOGIN_USERNAME)

    def get_flash_message(self):
        return self.wait_for_element(self.FLASH_MESSAGE).text