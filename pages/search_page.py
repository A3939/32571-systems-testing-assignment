from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SearchPage(BasePage):
    PRODUCT_CARD_SELECTOR = "#product-search .content-products .product-thumb"

    def open(self):
        return self.open_route("product/search")

    def search(self, query):
        self.fill("#input-search", query)
        self.click("#button-search")

    def product_cards(self):
        return self.driver.find_elements(By.CSS_SELECTOR, self.PRODUCT_CARD_SELECTOR)

    def product_titles(self):
        self.wait.until(lambda _: self.product_cards())
        title_elements = self.driver.find_elements(
            By.CSS_SELECTOR, f"{self.PRODUCT_CARD_SELECTOR} .title a"
        )
        return [element.text for element in title_elements]
