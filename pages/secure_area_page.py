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
        button = self.wait_for_clickable(self.LOGOUT_BUTTON)
        # Safari WebDriver can silently drop clicks on styled <a> elements;
        # JS click is more reliable across browsers
        self.driver.execute_script("arguments[0].click();", button)

    def wait_until_logged_out(self):
        # Safari can keep stale frame context after redirect
        try:
            self.driver.switch_to.default_content()
        except Exception:
            pass

        # Wait for the logout flash text — this is the single authoritative
        # signal that navigation completed and the page has fully rendered.
        # Using URL checks first was unreliable: the URL changed before the
        # new page's flash rendered, so get_flash_message() still saw the
        # stale "logged into" text from the previous page.
        self.wait_for_text_in_element(self.FLASH_MESSAGE, "You logged out of the secure area!")

    def get_flash_message(self):
        return self.wait_for_element(self.FLASH_MESSAGE).text