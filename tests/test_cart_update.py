import pytest

from pages.cart_page import CANON_EOS_5D, IPOD_CLASSIC, CartPage, ProductPurchasePage, added_message

pytestmark = pytest.mark.cart_update


def test_t006_s01_update_quantity(ipod_in_cart, checkpoint):
    cart = ipod_in_cart
    assert cart.rows()[IPOD_CLASSIC.name]["quantity"] == "1"
    checkpoint("before-update")

    cart.update_quantity(IPOD_CLASSIC.name, 3)
    cart.expect_text(".alert-success", CartPage.MODIFIED)
    row = cart.rows()[IPOD_CLASSIC.name]
    assert (row["quantity"], row["total"]) == ("3", "$366.00")
    totals = cart.totals()
    assert (totals["Sub-Total"], totals["Total"]) == ("$300.00", "$366.00")
    cart.expect_text("#cart-total", "3 item(s) - $366.00")


def test_t006_s02_remove_one_product(ipod_in_cart, driver, base_url, checkpoint):
    product = ProductPurchasePage(driver, base_url).open(CANON_EOS_5D.product_id)
    product.select_option("Select", "Red")
    assert product.add_to_cart() == added_message(CANON_EOS_5D)
    cart = CartPage(driver, base_url).open()
    assert sorted(cart.rows()) == sorted([CANON_EOS_5D.name, IPOD_CLASSIC.name])
    checkpoint("two-products")

    cart.remove(CANON_EOS_5D.name)
    rows = cart.rows()
    assert list(rows) == [IPOD_CLASSIC.name], "Remove deleted the wrong product or none"
    assert rows[IPOD_CLASSIC.name]["quantity"] == "1"
    assert cart.totals()["Total"] == IPOD_CLASSIC.price
    cart.expect_text("#cart-total", f"1 item(s) - {IPOD_CLASSIC.price}")


def test_t006_s03_zero_quantity_removes_item(ipod_in_cart, checkpoint):
    cart = ipod_in_cart
    checkpoint("before-update")

    cart.update_quantity(IPOD_CLASSIC.name, 0)
    cart.expect_text("#content", CartPage.EMPTY)
    assert cart.current_route() == "checkout/cart"
    assert cart.rows() == {}
    cart.expect_text("#cart-total", "0 item(s) - $0.00")
