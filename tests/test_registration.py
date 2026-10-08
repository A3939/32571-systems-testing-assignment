from uuid import uuid4
import pytest
from pages.account_page import RegistrationPage

pytestmark = pytest.mark.registration


def new_email():
    return f"uts-{uuid4().hex}@example.com"


@pytest.mark.creates_account
def test_t001_s01_valid_registration(driver, base_url):
    page = RegistrationPage(driver, base_url).open()
    page.complete(new_email())
    page.accept_policy()
    page.submit()
    page.expect_text("#content h1", "Your Account Has Been Created!")


def test_t001_s02_password_mismatch(driver, base_url):
    page = RegistrationPage(driver, base_url).open()
    page.complete(new_email(), confirm="Different!Pass123")
    page.accept_policy()
    page.submit()
    page.expect_text("#input-confirm + .text-danger", "Password confirmation does not match password!")


def test_t001_s03_policy_required(driver, base_url):
    page = RegistrationPage(driver, base_url).open()
    page.complete(new_email())
    page.submit()
    page.expect_text(".alert-danger", "You must agree to the Privacy Policy!")
