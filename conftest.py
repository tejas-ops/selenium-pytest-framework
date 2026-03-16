import os
import shutil
import tempfile
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from utils.config import BROWSER


@pytest.fixture
def driver(request):
    temp_profile_dir = None

    if BROWSER == "safari":
        browser = webdriver.Safari()

    elif BROWSER == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--incognito")

        temp_profile_dir = tempfile.mkdtemp(prefix="selenium-profile-")
        chrome_options.add_argument(f"--user-data-dir={temp_profile_dir}")

        if os.getenv("CI"):
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--remote-debugging-port=9222")

            if os.path.exists("/usr/bin/google-chrome"):
                chrome_options.binary_location = "/usr/bin/google-chrome"

        browser = webdriver.Chrome(service=ChromeService(), options=chrome_options)

    elif BROWSER == "firefox":
        browser = webdriver.Firefox()

    else:
        raise ValueError(f"Unsupported browser: {BROWSER}. Use safari, chrome, or firefox.")

    browser.maximize_window()
    yield browser

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs("screenshots", exist_ok=True)
        browser.save_screenshot(f"screenshots/{request.node.name}.png")

    browser.quit()
    time.sleep(1)

    if temp_profile_dir:
        shutil.rmtree(temp_profile_dir, ignore_errors=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)