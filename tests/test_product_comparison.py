import pytest

from pages.compare_page import ComparePage
from pages.product_page import ProductPage


pytestmark = pytest.mark.product_comparison


def add_product(driver, base_url, product_id):
    ProductPage(driver, base_url).open(product_id).add_to_compare()


def test_t008_s01_add_two_products(driver, base_url):
    add_product(driver, base_url, "43")
    add_product(driver, base_url, "44")
    names = ComparePage(driver, base_url).open().product_names()
    assert names == ["MacBook", "MacBook Air"]


def test_t008_s02_verify_comparison_details(driver, base_url):
    add_product(driver, base_url, "43")
    add_product(driver, base_url, "44")
    page = ComparePage(driver, base_url).open()

    assert page.product_names() == ["MacBook", "MacBook Air"]
    assert page.prices() == ["$602.00", "$1,202.00"]
    assert page.models() == ["Product 16", "Product 17"]
    assert page.brands() == ["Apple", "Apple"]
    assert page.availability() == ["Out Of Stock", "Out Of Stock"]


def test_t008_s03_add_third_product(driver, base_url):
    add_product(driver, base_url, "43")
    add_product(driver, base_url, "44")
    add_product(driver, base_url, "45")
    page = ComparePage(driver, base_url).open()

    assert page.product_names() == ["MacBook", "MacBook Air", "MacBook Pro"]
    assert page.prices() == ["$602.00", "$1,202.00", "$2,000.00"]
