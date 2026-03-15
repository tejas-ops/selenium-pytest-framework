from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import BASE_URL


class LoginPage(BasePage):
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH_MESSAGE = (By.ID, "flash")

    def open(self):
        self.driver.get(f"{BASE_URL}/login")

    def login(self, username, password):
        username_input = self.wait_for_element(self.USERNAME)
        password_input = self.wait_for_element(self.PASSWORD)
        username_input.clear()
        username_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)
        self.wait_for_clickable(self.LOGIN_BUTTON).click()

    def get_flash_message(self):
        return self.wait_for_element(self.FLASH_MESSAGE).text