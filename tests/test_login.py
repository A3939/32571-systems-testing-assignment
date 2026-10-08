from uuid import uuid4
import pytest
from pages.account_page import LoginPage

pytestmark = pytest.mark.login


def test_t002_s01_valid_login(credentials, driver, base_url):
    page = LoginPage(driver, base_url).open()
    page.login(*credentials)
    page.expect_text("#content h2", "My Account")
    assert "route=account/account" in driver.current_url


def test_t002_s02_unknown_account(driver, base_url):
    page = LoginPage(driver, base_url).open()
    page.login(f"unknown-{uuid4().hex}@example.com", "Wrong!Pass123")
    page.expect_text(".alert-danger", "No match for E-Mail Address and/or Password.")


def test_t002_s03_empty_credentials(driver, base_url):
    page = LoginPage(driver, base_url).open()
    page.login("", "")
    page.expect_text(".alert-danger", "No match for E-Mail Address and/or Password.")
