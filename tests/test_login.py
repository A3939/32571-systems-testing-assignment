from uuid import uuid4

import pytest

from pages.account_page import AccountPage, LoginPage

pytestmark = pytest.mark.login


@pytest.fixture
def login_page(driver, base_url):
    return LoginPage(driver, base_url).open()


def test_t002_s01_valid_login(credentials, login_page):
    login_page.login(*credentials)

    result = login_page.login_result()
    assert result == "authenticated", (
        f"Login was rejected: {result}. Check that the dedicated demo account "
        "is registered and that .env contains its correct credentials."
    )
    login_page.visible(AccountPage.LOGOUT_LINK)


def test_t002_s02_unknown_account(login_page):
    login_page.login(f"unknown-{uuid4().hex}@example.com", "Wrong!Pass123")

    login_page.expect_text(".alert-danger", "No match for E-Mail Address and/or Password.")
    assert login_page.current_route() == "account/login"


def test_t002_s03_empty_credentials(login_page):
    login_page.login("", "")

    login_page.expect_text(".alert-danger", "No match for E-Mail Address and/or Password.")
    assert login_page.current_route() == "account/login"
