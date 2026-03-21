import logging
import os
import shutil
import time

import pytest
import requests

from utils.config import BASE_URL
from utils.driver_factory import create_driver

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def check_base_url():
    """Warn if the UI base URL is unreachable before the test session starts."""
    try:
        response = requests.get(BASE_URL, timeout=10)
        if response.status_code >= 500:
            logger.warning("Base URL %s returned HTTP %s", BASE_URL, response.status_code)
        else:
            logger.info("Base URL %s is reachable (HTTP %s)", BASE_URL, response.status_code)
    except requests.ConnectionError:
        logger.warning("Base URL %s is not reachable — UI tests will likely fail", BASE_URL)


@pytest.fixture
def driver(request):
    browser, temp_profile_dir = create_driver()
    browser.maximize_window()
    yield browser

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/{request.node.name}.png"
        browser.save_screenshot(screenshot_path)
        logger.info("Screenshot saved: %s", screenshot_path)

    browser.quit()
    time.sleep(1)

    if temp_profile_dir:
        shutil.rmtree(temp_profile_dir, ignore_errors=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
