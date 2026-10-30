import hashlib
import json
import os
import secrets
from datetime import datetime, timezone
from pathlib import Path
import warnings
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from selenium import webdriver

from pages.account_page import AccountPage, RegistrationPage
from pages.cart_page import IPOD_CLASSIC, CartPage, ProductPurchasePage, added_message
from reporting.output import configure_report_paths

load_dotenv(Path(__file__).parent / ".env")

pytest_plugins = ["reporting.dashboard"]


def pytest_addoption(parser):
    parser.addoption("--browser", choices=["chrome", "firefox"], default="chrome")
    parser.addoption("--headless", action="store_true")
    parser.addoption("--base-url", default=os.getenv("BASE_URL", "https://opencart.abstracta.us"))
    parser.addoption("--allow-account-creation", action="store_true")
    parser.addoption("--screenshots", choices=["failed", "all", "none"], default="failed")
    parser.addoption("--evidence-dir", help="Run directory for screenshots and the default report")


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    configure_report_paths(config)


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
def registered_account(request, driver, base_url):
    """Prepare a dedicated account without relying on any other test's run."""
    if not request.config.getoption("--allow-account-creation"):
        pytest.skip("Use --allow-account-creation to prepare a dedicated synthetic account")
    email, password = f"uts-{uuid4().hex}@example.com", secrets.token_urlsafe(12)
    page = RegistrationPage(driver, base_url).open()
    page.complete(email, password=password)
    page.accept_policy()
    page.submit()
    page.expect_text("#content", "Congratulations! Your new account has been successfully created!")
    assert page.current_route() == "account/success", "Account prerequisite did not reach success"
    AccountPage(driver, base_url).logout()
    page.expect_text("#content", "You have been logged off your account.")
    assert page.current_route() == "account/logout", "Account prerequisite did not log out"
    return email, password


@pytest.fixture
def ipod_in_cart(driver, base_url):
    """Start from a cart holding one iPod Classic, added through the T005 add-to-cart flow."""
    product = ProductPurchasePage(driver, base_url).open(IPOD_CLASSIC.product_id)
    message = product.add_to_cart()
    assert message == added_message(IPOD_CLASSIC), f"Cart prerequisite was not added: {message}"
    product.expect_text("#cart-total", f"1 item(s) - {IPOD_CLASSIC.price}")
    return CartPage(driver, base_url).open()


@pytest.fixture
def checkpoint(request, driver):
    """Capture intermediate lifecycle states when all evidence is requested."""
    def capture(step):
        if request.config.getoption("--screenshots") != "all":
            return
        directory = Path(request.config.getoption("--evidence-dir")) / "steps"
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{request.node.name}-{step}.png"
        driver.save_screenshot(str(path))
        request.node.user_properties.append((f"step_{step}", driver.current_url))
    return capture


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
        directory = Path(item.config.getoption("--evidence-dir")) / "screenshots"
        directory.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
        digest = hashlib.sha256(item.nodeid.encode()).hexdigest()[:10]
        path = directory / f"{stamp}-{digest}.png"
        browser.save_screenshot(str(path))
        item._dashboard_screenshot = browser.get_screenshot_as_base64()
        observations = [
            ("screenshot", str(path)),
            ("observed_url", browser.current_url),
            ("observed_heading", " | ".join(e.text for e in browser.find_elements("css selector", "#content h1"))),
            ("observed_alert", " | ".join(e.text for e in browser.find_elements("css selector", ".alert-danger, .alert-success") if e.is_displayed())),
        ]
        item.user_properties.extend(observations)
        path.with_suffix(".json").write_text(json.dumps(dict(observations), indent=2) + "\n")
        if item.config.pluginmanager.hasplugin("html"):
            from pytest_html import extras
            report.extras = getattr(report, "extras", []) + [
                extras.png(browser.get_screenshot_as_base64(), name="Browser screenshot")]
    except Exception as exc:
        warnings.warn(f"Could not capture screenshot: {exc}", stacklevel=1)
