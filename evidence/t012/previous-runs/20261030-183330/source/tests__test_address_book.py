"""T012 / F12 Address book (Member 4).

Each scenario uses its own synthetic account (logged_in_account fixture). A new account
has no saved address, so every address here is created by the test itself.
Synthetic address data only.
"""
import pytest

from pages.member4_account_pages import AddressBookPage, AddressFormPage

pytestmark = [pytest.mark.address_book, pytest.mark.creates_account]

HOME = dict(firstname="Study", lastname="Tester", address_1="15 Broadway", city="Ultimo",
            postcode="2007", country="Australia", zone="New South Wales")
WORK = dict(firstname="Study", lastname="Office", company="UTS", address_1="81 Broadway",
            city="Ultimo", postcode="2007", country="Australia", zone="New South Wales")


def add_address(driver, base_url, data, default):
    form = AddressFormPage(driver, base_url).open_new()
    form.fill_address(**data)
    form.set_default(default)
    form.submit()
    book = AddressBookPage(driver, base_url)
    assert "Your address has been successfully added" in book.alert()
    return book


def test_t012_s01_add_valid_address(logged_in_account, driver, base_url, checkpoint):
    book = AddressBookPage(driver, base_url).open()
    assert "You have no addresses in your account." in book.content_text()
    book.click_new()
    form = AddressFormPage(driver, base_url)
    assert form.current_route() == "account/address/add"
    form.fill_address(**HOME)
    checkpoint("filled")
    form.submit()

    assert "Your address has been successfully added" in book.alert()
    assert book.current_route() == "account/address"
    assert len(book.entries()) == 1
    entry = book.entries()[0]
    for part in ("Study Tester", "15 Broadway", "Ultimo 2007", "New South Wales", "Australia"):
        assert part in entry, f"{part!r} missing from saved address: {entry!r}"


def test_t012_s02_missing_mandatory_fields(logged_in_account, driver, base_url, checkpoint):
    form = AddressFormPage(driver, base_url).open_new()
    form.submit()
    errors = form.wait_for_errors()
    checkpoint("validation")
    expected = {
        "First Name": "First Name must be between 1 and 32 characters!",
        "Last Name": "Last Name must be between 1 and 32 characters!",
        "Address 1": "Address must be between 3 and 128 characters!",
        "City": "City must be between 2 and 128 characters!",
        "Region / State": "Please select a region / state!",
    }
    for label, message in expected.items():
        assert errors.get(label) == message, f"{label}: expected {message!r}, got {errors.get(label)!r}; all={errors}"
    assert "Company" not in errors and "Address 2" not in errors, f"Optional field flagged: {errors}"
    assert form.current_route() == "account/address/add"

    book = AddressBookPage(driver, base_url).open()
    assert "You have no addresses in your account." in book.content_text(), "Invalid address was saved"


def test_t012_s03_edit_then_delete_address(logged_in_account, driver, base_url, checkpoint):
    add_address(driver, base_url, HOME, default=True)
    book = add_address(driver, base_url, WORK, default=False)
    assert len(book.entries()) == 2
    checkpoint("two-addresses")

    book.click_edit("81 Broadway")
    form = AddressFormPage(driver, base_url)
    assert form.value("address-1") == "81 Broadway"
    form.fill_address(address_1="1 Harris Street", city="Pyrmont")
    form.submit()
    assert "Your address has been successfully updated" in book.alert()
    assert any("1 Harris Street" in e and "Pyrmont 2007" in e for e in book.entries()), book.entries()
    assert not any("81 Broadway" in e for e in book.entries())
    checkpoint("edited")

    book.click_delete("1 Harris Street")
    assert "Your address has been successfully deleted" in book.alert()
    entries = book.entries()
    assert len(entries) == 1 and "15 Broadway" in entries[0], entries
    checkpoint("deleted")

    book.click_delete("15 Broadway")
    assert "Warning:" in book.alert("warning, .alert-danger"), "Deleting the only (default) address should be refused"
    assert len(book.entries()) == 1
