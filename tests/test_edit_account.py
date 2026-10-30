"""T011 / F11 Edit account information (Member 4).

Each scenario uses its own synthetic account (logged_in_account fixture), so changes
never touch another tester's data and the tests do not depend on pytest order.
The fixture registers every account as Study / Tester / 0412345678.
"""
from uuid import uuid4

import pytest

from pages.member4_account_pages import AccountMenu, EditAccountPage

pytestmark = [pytest.mark.edit_account, pytest.mark.creates_account]

ORIGINAL = {"firstname": "Study", "lastname": "Tester", "telephone": "0412345678"}


def test_t011_s01_update_name_and_telephone(logged_in_account, driver, base_url, checkpoint):
    email = logged_in_account[0]
    page = EditAccountPage(driver, base_url).open()
    assert page.values() == {**ORIGINAL, "email": email}
    checkpoint("before")

    page.update(firstname="Updated", lastname="Member Four", telephone="0298765432")
    menu = AccountMenu(driver, base_url)
    assert "Success: Your account has been successfully updated." in menu.success_alert()
    assert menu.current_route() == "account/account"
    checkpoint("success")

    page.open()
    assert page.values() == {"firstname": "Updated", "lastname": "Member Four",
                             "telephone": "0298765432", "email": email}, "Changes were not saved"


def test_t011_s02_empty_first_name_rejected(logged_in_account, driver, base_url, checkpoint):
    email = logged_in_account[0]
    page = EditAccountPage(driver, base_url).open()
    page.update(firstname="")
    errors = page.wait_for_errors()
    assert errors == {"firstname": "First Name must be between 1 and 32 characters!"}, errors
    assert page.current_route() == "account/edit"
    checkpoint("validation")

    page.open()
    assert page.values() == {**ORIGINAL, "email": email}, "Rejected edit changed the saved details"


def test_t011_s03_invalid_email_rejected(logged_in_account, driver, base_url, checkpoint):
    email = logged_in_account[0]
    invalid = f"member4-{uuid4().hex[:8]}@"
    page = EditAccountPage(driver, base_url).open()

    # Layer 1: the browser's own check on the type="email" field blocks the submit.
    page.update(email=invalid)
    valid, message = page.browser_validation("email")
    assert not valid and message, "Browser accepted an incomplete email"
    assert page.current_route() == "account/edit"
    assert not driver.find_elements("css selector", ".alert-success"), "Invalid email was reported as saved"
    checkpoint("browser-validation")

    # Layer 2: with the browser check skipped, the server must still reject it.
    page.disable_browser_validation()
    page.update(email=invalid)
    errors = page.wait_for_errors()
    assert errors == {"email": "E-Mail Address does not appear to be valid!"}, errors
    assert page.current_route() == "account/edit"
    checkpoint("server-validation")

    page.open()
    assert page.values()["email"] == email, "Rejected email replaced the saved address"
