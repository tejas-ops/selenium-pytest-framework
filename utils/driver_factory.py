import logging
import os
import tempfile

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from utils.config import BROWSER

logger = logging.getLogger(__name__)


def create_driver():
    """Create and return a (WebDriver, temp_profile_dir) tuple based on BROWSER env var."""
    logger.info("Creating driver for browser: %s", BROWSER)
    if BROWSER == "safari":
        return webdriver.Safari(), None
    elif BROWSER == "chrome":
        return _create_chrome_driver()
    elif BROWSER == "firefox":
        return _create_firefox_driver(), None
    else:
        raise ValueError(f"Unsupported browser: {BROWSER}. Use safari, chrome, or firefox.")


def _create_chrome_driver():
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

    logger.debug("Chrome profile dir: %s", temp_profile_dir)
    return webdriver.Chrome(service=ChromeService(), options=chrome_options), temp_profile_dir


def _create_firefox_driver():
    firefox_options = FirefoxOptions()
    if os.getenv("CI"):
        firefox_options.add_argument("--headless")
    return webdriver.Firefox(options=firefox_options)
