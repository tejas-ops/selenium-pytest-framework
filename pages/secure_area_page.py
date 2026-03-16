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
        logout_button = self.wait_for_clickable(self.LOGOUT_BUTTON)
        try:
            logout_button.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", logout_button)

    def wait_until_logged_out(self):
        self.wait.until(
            EC.any_of(
                EC.presence_of_element_located(self.LOGIN_USERNAME),
                EC.text_to_be_present_in_element(self.FLASH_MESSAGE, "You logged out of the secure area!"),
                EC.url_contains("/login"),
                EC.url_contains("/authenticate"),
                EC.invisibility_of_element_located(self.LOGOUT_BUTTON),
            )
        )

    def get_flash_message(self):
        return self.wait_for_element(self.FLASH_MESSAGE).text