import pytest
import allure
from pages.login_page import LoginPage
from pages.secure_area_page import SecureAreaPage
from utils.data_loader import load_json

login_data = load_json("login_data.json")
valid_login = login_data["valid_login"]
invalid_login_cases = login_data["invalid_login_cases"]

@pytest.mark.smoke
@allure.feature("Login")
@allure.story("Valid login")
def test_valid_login(driver):
    with allure.step("Open login page"):
        login_page = LoginPage(driver)
        login_page.open()

    with allure.step("Login with valid credentials"):
        login_page.login(valid_login["username"], valid_login["password"])

    with allure.step("Wait for secure area to load"):
        secure_page = SecureAreaPage(driver)
        secure_page.wait_until_loaded()

    with allure.step("Verify successful login"):
        assert "You logged into a secure area!" in login_page.get_flash_message()
        assert "/secure" in secure_page.get_current_url()


@pytest.mark.regression
@pytest.mark.parametrize(
    "username,password,expected_message",
    [
        (case["username"], case["password"], case["expected_message"])
        for case in invalid_login_cases
    ],
)
@allure.feature("Login")
@allure.story("Invalid login")
def test_invalid_login(driver, username, password, expected_message):

    with allure.step("Open login page"):
        login_page = LoginPage(driver)
        login_page.open()

    with allure.step("Attempt login with invalid credentials"):
        login_page.login(username, password)

    with allure.step("Verify error message and URL"):
        assert expected_message in login_page.get_flash_message()
        assert "/login" in login_page.get_current_url()


@pytest.mark.regression
@allure.feature("Login")
@allure.story("Logout")
def test_logout(driver):

    with allure.step("Initialize pages"):
        login_page = LoginPage(driver)
        secure_page = SecureAreaPage(driver)

    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Login with valid credentials"):
        login_page.login(valid_login["username"], valid_login["password"])

    with allure.step("Wait for secure area page"):
        secure_page.wait_until_loaded()

    with allure.step("Click logout"):
        secure_page.click_logout()

    with allure.step("Wait for logged out state and verify flash"):
        # wait_until_logged_out blocks until the logout flash text is present,
        # so we don't read it again — re-reading races with auto-dismiss in Safari
        secure_page.wait_until_logged_out()

    with allure.step("Verify redirected to login page"):
        current_url = secure_page.get_current_url()
        assert "/login" in current_url or "/authenticate" in current_url


@pytest.mark.smoke
@allure.feature("Login")
@allure.story("Login page title")
def test_login_page_title(driver):

    with allure.step("Open login page"):
        login_page = LoginPage(driver)
        login_page.open()

    with allure.step("Verify title and URL"):
        assert "The Internet" in login_page.get_title()
        assert "/login" in login_page.get_current_url()