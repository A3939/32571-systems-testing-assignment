import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
import warnings

import pytest
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()

pytest_plugins = ["reporting.dashboard"]


def pytest_addoption(parser):
    parser.addoption("--browser", choices=["chrome", "firefox"], default="chrome")
    parser.addoption("--headless", action="store_true")
    parser.addoption("--base-url", default=os.getenv("BASE_URL", "https://ecommerce-playground.lambdatest.io"))
    parser.addoption("--allow-account-creation", action="store_true")
    parser.addoption("--screenshots", choices=["failed", "all", "none"], default="failed")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--allow-account-creation"):
        for item in items:
            if item.get_closest_marker("creates_account"):
                item.add_marker(pytest.mark.skip(reason="Use --allow-account-creation to create a demo account"))


@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    options = webdriver.ChromeOptions() if browser == "chrome" else webdriver.FirefoxOptions()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new" if browser == "chrome" else "-headless")
    factory = webdriver.Chrome if browser == "chrome" else webdriver.Firefox
    instance = factory(options=options)
    request.node._browser = instance
    try:
        instance.set_window_size(1440, 1000)
        instance.set_page_load_timeout(45)
        yield instance
    finally:
        instance.quit()


@pytest.fixture
def credentials():
    email, password = os.getenv("TEST_EMAIL"), os.getenv("TEST_PASSWORD")
    if not email or not password:
        pytest.skip("Set TEST_EMAIL and TEST_PASSWORD in .env for a registered demo account")
    return email, password


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    mode = item.config.getoption("--screenshots")
    capture = (report.failed and report.when in ("setup", "call")) or (mode == "all" and report.when == "call" and not report.skipped)
    browser = getattr(item, "_browser", None)
    if mode == "none" or not capture or browser is None:
        return
    try:
        directory = Path("reports/screenshots")
        directory.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
        digest = hashlib.sha256(item.nodeid.encode()).hexdigest()[:10]
        path = directory / f"{stamp}-{digest}.png"
        browser.save_screenshot(str(path))
        item._dashboard_screenshot = browser.get_screenshot_as_base64()
        if item.config.pluginmanager.hasplugin("html"):
            from pytest_html import extras
            report.extras = getattr(report, "extras", []) + [
                extras.png(browser.get_screenshot_as_base64(), name="Browser screenshot")]
    except Exception as exc:
        warnings.warn(f"Could not capture screenshot: {exc}", stacklevel=1)
