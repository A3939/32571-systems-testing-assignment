import pytest

from pages.cart_page import CANON_EOS_5D, IPOD_CLASSIC, CartPage, ProductPurchasePage, added_message

pytestmark = pytest.mark.add_to_cart

EMPTY_HEADER = "0 item(s) - $0.00"


def test_t005_s01_add_simple_product(driver, base_url, checkpoint):
    product = ProductPurchasePage(driver, base_url).open(IPOD_CLASSIC.product_id)
    assert product.name() == IPOD_CLASSIC.name
    assert product.cart_total() == EMPTY_HEADER

    assert product.add_to_cart() == added_message(IPOD_CLASSIC)
    product.expect_text("#cart-total", f"1 item(s) - {IPOD_CLASSIC.price}")
    checkpoint("added")

    cart = CartPage(driver, base_url).open()
    row = cart.rows()[IPOD_CLASSIC.name]
    assert list(cart.rows()) == [IPOD_CLASSIC.name]
    assert (row["quantity"], row["unit_price"], row["total"]) == ("1", IPOD_CLASSIC.price, IPOD_CLASSIC.price)
    assert not cart.has_stock_warning(), "An in-stock product was flagged as unavailable"


def test_t005_s02_required_option(driver, base_url, checkpoint):
    product = ProductPurchasePage(driver, base_url).open(CANON_EOS_5D.product_id)
    assert product.add_to_cart() == "Select required!"
    assert product.cart_total() == EMPTY_HEADER, "A product was added without its required option"
    checkpoint("option-required")

    product.select_option("Select", "Red")
    assert product.add_to_cart() == added_message(CANON_EOS_5D)
    product.expect_text("#cart-total", f"1 item(s) - {CANON_EOS_5D.price}")

    cart = CartPage(driver, base_url).open()
    row = cart.rows()[CANON_EOS_5D.name]
    assert "Select: Red" in row["details"]
    assert (row["quantity"], row["total"]) == ("1", CANON_EOS_5D.price)


def test_t005_s03_zero_quantity(driver, base_url, checkpoint):
    product = ProductPurchasePage(driver, base_url).open(IPOD_CLASSIC.product_id)
    product.set_quantity(0)
    message = product.add_to_cart()
    checkpoint("add-response")

    cart = CartPage(driver, base_url).open()
    cart.expect_text("#content", CartPage.EMPTY)
    assert cart.cart_total() == EMPTY_HEADER
    assert not message.startswith("Success"), (
        f"Quantity 0 added nothing, but the product page confirmed: {message!r}")
