import pytest

from pages.product_page import ProductPage


pytestmark = pytest.mark.product_details


def test_t004_s01_product_identity(driver, base_url):
    page = ProductPage(driver, base_url).open("43")
    assert page.name() == "MacBook"
    assert page.main_image_alt() == "MacBook"
    assert "product_id=43" in driver.current_url


def test_t004_s02_price_and_availability(driver, base_url):
    page = ProductPage(driver, base_url).open("43")
    assert page.price() == "$602.00"
    assert page.availability() == "Out Of Stock"


def test_t004_s03_required_option(driver, base_url):
    page = ProductPage(driver, base_url).open("30")
    selector = "#input-option226"
    assert page.name() == "Canon EOS 5D"
    assert page.option_label(selector) == "Select"
    assert page.option_choices(selector) == ["--- Please Select ---", "Red", "Blue"]
    assert page.select_option(selector, "Blue") == "Blue"
