"""T007 / F07 Wish list (Member 4).

Each scenario starts in a fresh browser with its own synthetic account, created and
logged in by the logged_in_account fixture (F01 + F02), so no test depends on pytest order.
Product data (iPhone id 40, MacBook id 43) comes from the F04 product pages.
"""
import pytest

from pages.account_page import AccountPage, LoginPage
from pages.member4_account_pages import AccountMenu, ProductWishPage, WishListPage

pytestmark = [pytest.mark.wishlist, pytest.mark.creates_account]

IPHONE, MACBOOK = 40, 43


def test_t007_s01_add_product_to_wishlist(logged_in_account, driver, base_url, checkpoint):
    wishlist = WishListPage(driver, base_url).open()
    assert wishlist.product_names() == [], "A new account should start with no wish-list products"

    product = ProductWishPage(driver, base_url).open(IPHONE)
    assert product.product_name() == "iPhone"
    alert = product.add_to_wishlist()
    assert "Success: You have added iPhone to your wish list!" in alert, alert
    product.wait_header_wishlist_total("Wish List (1)")
    checkpoint("added-alert")

    wishlist.open()
    assert wishlist.current_route() == "account/wishlist"
    assert wishlist.product_names() == ["iPhone"]
    row = wishlist.row("iPhone")
    assert (row["model"], row["stock"], row["price"]) == ("product 11", "In Stock", "$123.20"), row


def test_t007_s02_wishlist_persists_after_logout(logged_in_account, driver, base_url, checkpoint):
    for product_id in (IPHONE, MACBOOK):
        ProductWishPage(driver, base_url).open(product_id).add_to_wishlist()
    ProductWishPage(driver, base_url).wait_header_wishlist_total("Wish List (2)")
    checkpoint("two-added")

    account = AccountPage(driver, base_url).open()
    account.logout()
    account.expect_text("#content", "You have been logged off your account.")
    WishListPage(driver, base_url).open()
    assert WishListPage(driver, base_url).current_route() == "account/login", "Wish list was visible after logout"
    checkpoint("logged-out-redirect")

    page = LoginPage(driver, base_url).open()
    page.login(*logged_in_account)
    assert page.login_result() == "authenticated"
    menu = AccountMenu(driver, base_url).open()
    menu.go_to("account/wishlist")
    wishlist = WishListPage(driver, base_url)
    wishlist.wait.until(lambda d: wishlist.current_route() == "account/wishlist", "Wish list link did not open the wish list")
    assert sorted(wishlist.product_names()) == ["MacBook", "iPhone"]
    wishlist.expect_text("#wishlist-total", "Wish List (2)")


def test_t007_s03_remove_products_from_wishlist(logged_in_account, driver, base_url, checkpoint):
    for product_id in (IPHONE, MACBOOK):
        ProductWishPage(driver, base_url).open(product_id).add_to_wishlist()
    wishlist = WishListPage(driver, base_url).open()
    assert sorted(wishlist.product_names()) == ["MacBook", "iPhone"]
    checkpoint("before-remove")

    wishlist.remove("iPhone")
    assert "Success: You have modified your wish list!" in wishlist.success_alert()
    assert wishlist.product_names() == ["MacBook"]
    wishlist.expect_text("#wishlist-total", "Wish List (1)")
    checkpoint("one-removed")

    wishlist.remove("MacBook")
    assert "Success: You have modified your wish list!" in wishlist.success_alert()
    assert wishlist.product_names() == []
    assert "Your wish list is empty." in wishlist.content_text()
    wishlist.expect_text("#wishlist-total", "Wish List (0)")
