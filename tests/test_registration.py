from uuid import uuid4

import pytest

from pages.account_page import RegistrationPage

pytestmark = pytest.mark.registration


def new_email():
    return f"uts-{uuid4().hex}@example.com"


@pytest.fixture
def registration_page(driver, base_url):
    return RegistrationPage(driver, base_url).open()


@pytest.mark.creates_account
def test_t001_s01_valid_registration(registration_page):
    registration_page.complete(new_email())
    registration_page.accept_policy()
    registration_page.submit()

    registration_page.expect_text("#content h1", "Your Account Has Been Created!")


def test_t001_s02_password_mismatch(registration_page):
    registration_page.complete(new_email(), confirm="Different!Pass123")
    registration_page.accept_policy()
    registration_page.submit()

    registration_page.expect_text(
        "#input-confirm + .text-danger",
        "Password confirmation does not match password!",
    )


def test_t001_s03_policy_required(registration_page):
    registration_page.complete(new_email())
    registration_page.submit()

    registration_page.expect_text(".alert-danger", "You must agree to the Privacy Policy!")
