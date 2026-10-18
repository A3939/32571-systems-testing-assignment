import pytest

from pages.account_page import AccountPage, LoginPage

pytestmark = pytest.mark.logout


@pytest.fixture
def account_page(credentials, driver, base_url):
    login_page = LoginPage(driver, base_url).open()
    login_page.login(*credentials)
    result = login_page.login_result()
    assert result == "authenticated", f"Logout prerequisite failed: login returned {result}"

    page = AccountPage(driver, base_url)
    page.visible(AccountPage.LOGOUT_LINK)
    return page


def test_t009_s01_logout_authenticated_session(account_page):
    account_page.logout()

    account_page.expect_text("#content h1", "Account Logout")
    account_page.expect_text("#content", "You have been logged off your account.")
    assert account_page.current_route() == "account/logout"


def test_t009_s02_protected_account_after_logout(account_page):
    account_page.logout()
    account_page.expect_text("#content h1", "Account Logout")

    account_page.open()

    account_page.visible("#input-email")
    account_page.visible("#input-password")
    assert account_page.current_route() == "account/login", (
        "Protected account navigation should redirect to login after logout"
    )


def test_t009_s03_login_again_after_logout(account_page, credentials, driver, base_url):
    account_page.logout()
    account_page.expect_text("#content h1", "Account Logout")

    login_page = LoginPage(driver, base_url).open()
    login_page.login(*credentials)

    result = login_page.login_result()
    assert result == "authenticated", f"Login after logout was rejected: {result}"
    login_page.visible(AccountPage.LOGOUT_LINK)
