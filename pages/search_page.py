from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SearchPage(BasePage):
    def open(self):
        return self.open_route("product/search")

    def search(self, query):
        self.fill("#input-search", query)
        self.click("#button-search")

    def product_titles(self):
        self.wait.until(
            lambda d: d.find_elements(
                By.CSS_SELECTOR,
                ".product-layout .product-thumb",
            )
        )
        return [
            element.text
            for element in self.driver.find_elements(
                By.CSS_SELECTOR,
                ".product-thumb .caption h4 a",
            )
        ]

    def no_results_message(self):
        return self.visible("#content h2 + p").text
