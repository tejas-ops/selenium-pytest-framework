import pytest
from pages.login_page import LoginPage
from pages.secure_area_page import SecureAreaPage
from utils.test_data import VALID_USERNAME, VALID_PASSWORD, INVALID_LOGIN_CASES


@pytest.mark.smoke
def test_valid_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    secure_page = SecureAreaPage(driver)
    secure_page.wait_until_loaded()

    assert "You logged into a secure area!" in login_page.get_flash_message()
    assert "/secure" in secure_page.get_current_url()


@pytest.mark.regression
@pytest.mark.parametrize("username,password,expected_message", INVALID_LOGIN_CASES)
def test_invalid_login(driver, username, password, expected_message):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(username, password)

    assert expected_message in login_page.get_flash_message()
    assert "/login" in login_page.get_current_url()


@pytest.mark.regression
def test_logout(driver):
    login_page = LoginPage(driver)
    secure_page = SecureAreaPage(driver)

    login_page.open()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    secure_page.wait_until_loaded()
    secure_page.click_logout()

    assert "/login" in secure_page.get_current_url() or "/authenticate" in secure_page.get_current_url()
    assert "You logged out of the secure area!" in secure_page.get_flash_message()


@pytest.mark.smoke
def test_login_page_title(driver):
    login_page = LoginPage(driver)
    login_page.open()

    assert "The Internet" in login_page.get_title()
    assert "/login" in login_page.get_current_url()