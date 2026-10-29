import pytest
from selenium.webdriver.common.by import By

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

pytestmark = pytest.mark.checkout

GUEST = {
    "firstname": "Study", "lastname": "Tester", "email": "study.tester@example.com",
    "telephone": "0412345678", "address-1": "15 Broadway", "city": "Ultimo", "postcode": "2007",
    "country": "Australia", "zone": "New South Wales",
}


def test_t010_s01_empty_cart_redirect(driver, base_url):
    page = CheckoutPage(driver, base_url).open()
    page.expect_text("#content", CartPage.EMPTY)
    assert page.current_route() == "checkout/cart", "Checkout opened without any products"
    assert not driver.find_elements(By.ID, "button-account")
    assert page.cart_total() == "0 item(s) - $0.00"


def test_t010_s02_blank_guest_details(ipod_in_cart, driver, base_url, checkpoint):
    page = CheckoutPage(driver, base_url).open()
    page.continue_as_guest()
    checkpoint("guest-form")

    page.submit_guest_details()
    assert page.field_errors() == CheckoutPage.BLANK_GUEST_ERRORS
    assert page.open_steps() == ["collapse-payment-address"], "Checkout advanced past invalid billing details"


def test_t010_s03_invalid_email_then_corrected(ipod_in_cart, driver, base_url, checkpoint):
    page = CheckoutPage(driver, base_url).open()
    page.continue_as_guest()
    page.fill_guest_details({**GUEST, "email": "study.tester@"})
    page.submit_guest_details()
    assert page.field_errors() == {"email": CheckoutPage.BLANK_GUEST_ERRORS["email"]}
    assert page.open_steps() == ["collapse-payment-address"]
    checkpoint("invalid-email")

    page.fill("#input-payment-email", GUEST["email"])
    page.submit_guest_details()
    page.expect_text(CheckoutPage.DELIVERY_METHOD, "Flat Shipping Rate")
    assert page.open_steps() == ["collapse-shipping-method"]
    assert page.visible_field_errors() == []
