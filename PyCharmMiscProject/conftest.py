import os
import pytest
from selenium import webdriver
from utils.config import BROWSER


@pytest.fixture
def driver(request):
    if BROWSER == "safari":
        browser = webdriver.Safari()
    elif BROWSER == "chrome":
        browser = webdriver.Chrome()
    else:
        raise ValueError(f"Unsupported browser: {BROWSER}")

    browser.maximize_window()
    yield browser

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs("screenshots", exist_ok=True)
        browser.save_screenshot(f"screenshots/{request.node.name}.png")

    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)