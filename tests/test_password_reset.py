from uuid import uuid4

import pytest

from pages.account_page import AccountPage
from pages.password_reset_page import PasswordResetPage

pytestmark = pytest.mark.password_reset


@pytest.fixture
def reset_page(driver, base_url):
    page = PasswordResetPage(driver, base_url).open()
    page.expect_text("#content", "Enter the e-mail address associated with your account.")
    page.visible("#input-email")
    assert page.current_route() == "account/forgotten"
    return page


@pytest.mark.creates_account
def test_t009_s01_registered_email(registered_account, reset_page):
    # One request to this dedicated fixture account; email delivery is out of scope.
    reset_page.request_reset(registered_account[0])

    reset_page.expect_text(".alert-success", PasswordResetPage.CONFIRMATION)
    assert reset_page.current_route() == "account/login"
    reset_page.visible("#input-email")
    reset_page.visible("#input-password")
    assert not reset_page.driver.find_elements("css selector", AccountPage.LOGOUT_LINK)


def test_t009_s02_unregistered_email(reset_page):
    reset_page.request_reset(f"unknown-{uuid4().hex}@example.com")

    reset_page.expect_text(".alert-danger", PasswordResetPage.UNKNOWN_EMAIL)
    assert reset_page.current_route() == "account/forgotten"
    assert not reset_page.driver.find_elements("css selector", ".alert-success")


def test_t009_s03_empty_email(reset_page):
    reset_page.request_reset("")

    reset_page.expect_text(".alert-danger", PasswordResetPage.UNKNOWN_EMAIL)
    assert reset_page.current_route() == "account/forgotten"
    assert not reset_page.driver.find_elements("css selector", ".alert-success")
