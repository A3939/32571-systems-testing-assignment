from uuid import uuid4
import pytest
from pages.search_page import SearchPage

pytestmark = pytest.mark.search


@pytest.mark.parametrize("query, expected", [("iPhone", "iphone"), ("MacBook", "macbook")],
                         ids=["T003-S01-iPhone", "T003-S02-MacBook"])
def test_t003_existing_product(driver, base_url, query, expected):
    page = SearchPage(driver, base_url).open()
    page.search(query)
    titles = page.product_titles()
    assert titles, "Expected visible product titles"
    assert any(expected in title.lower() for title in titles), titles


def test_t003_s03_no_results(driver, base_url):
    page = SearchPage(driver, base_url).open()
    page.search(f"no-such-product-{uuid4().hex}")
    page.expect_text("#product-search .content-products", "There is no product that matches the search criteria.")
    assert not driver.find_elements("css selector", "#product-search .content-products .product-thumb")
