from selenium.webdriver.common.by import By
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

    def wait_until_logged_out(self):
        # Safari can keep stale frame context after redirect
        try:
            self.driver.switch_to.default_content()
        except Exception:
            pass

        # Wait for navigation away from the secure area first
        self.wait.until(
            EC.any_of(
                EC.url_contains("/login"),
                EC.url_contains("/authenticate"),
            )
        )
        # Then wait specifically for the logout flash — resolving on URL alone
        # caused get_flash_message() to read stale "logged in" text in Safari
        self.wait_for_text_in_element(self.FLASH_MESSAGE, "You logged out of the secure area!")

    def get_flash_message(self):
        return self.wait_for_element(self.FLASH_MESSAGE).text