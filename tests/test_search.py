from uuid import uuid4

import pytest

from pages.search_page import SearchPage

pytestmark = pytest.mark.search


@pytest.fixture
def search_page(driver, base_url):
    return SearchPage(driver, base_url).open()


@pytest.mark.parametrize(
    "query",
    [
        pytest.param("iPhone", id="T003-S01-iPhone"),
        pytest.param("MacBook", id="T003-S02-MacBook"),
    ],
)
def test_t003_existing_product(search_page, query):
    search_page.search(query)

    titles = search_page.product_titles()
    assert titles, "Expected visible product titles"
    assert any(query.lower() in title.lower() for title in titles), (
        f"Expected a product title containing {query!r}, but found: {titles}"
    )


def test_t003_s03_no_results(search_page):
    search_page.search(f"no-such-product-{uuid4().hex}")

    search_page.expect_text(
        "#product-search .content-products",
        "There is no product that matches the search criteria.",
    )
    assert not search_page.product_cards(), "Expected no product cards for an unknown product"
