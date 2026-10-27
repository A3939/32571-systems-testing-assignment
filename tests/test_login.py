from uuid import uuid4
import pytest
from pages.account_page import AccountPage, LoginPage

pytestmark = pytest.mark.login


@pytest.mark.creates_account
def test_t002_s01_valid_login(registered_account, driver, base_url, checkpoint):
    page = LoginPage(driver, base_url).open()
    page.login(*registered_account)
    result = page.login_result()
    assert result == "authenticated", (
        f"Login was rejected: {result}. Check that the dedicated demo account "
        "was successfully prepared in this test's fixture."
    )
    page.visible(AccountPage.LOGOUT_LINK)
    checkpoint("login")

    account = AccountPage(driver, base_url).open()
    assert account.current_route() == "account/account"
    account.visible(AccountPage.LOGOUT_LINK)
    checkpoint("account-access")

    account.logout()
    account.expect_text("#content", "You have been logged off your account.")
    assert account.current_route() == "account/logout"
    checkpoint("logout")

    account.open()
    account.visible("#input-email")
    account.visible("#input-password")
    assert account.current_route() == "account/login", "Protected account access survived logout"
    checkpoint("protected-route")

    page.open().login(*registered_account)
    assert page.login_result() == "authenticated", "Fresh login after logout was rejected"
    page.visible(AccountPage.LOGOUT_LINK)
    checkpoint("fresh-login")


def test_t002_s02_unknown_account(driver, base_url, checkpoint):
    page = LoginPage(driver, base_url).open()
    page.login(f"unknown-{uuid4().hex}@example.com", "Wrong!Pass123")
    page.expect_text(".alert-danger", "No match for E-Mail Address and/or Password.")
    assert page.current_route() == "account/login"
    checkpoint("rejection")
    AccountPage(driver, base_url).open()
    page.visible("#input-email")
    assert page.current_route() == "account/login", "Rejected credentials granted account access"


def test_t002_s03_empty_credentials(driver, base_url, checkpoint):
    page = LoginPage(driver, base_url).open()
    page.login("", "")
    page.expect_text(".alert-danger", "No match for E-Mail Address and/or Password.")
    assert page.current_route() == "account/login"
    checkpoint("rejection")
    AccountPage(driver, base_url).open()
    page.visible("#input-email")
    assert page.current_route() == "account/login", "Empty credentials granted account access"
