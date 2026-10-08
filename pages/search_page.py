from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SearchPage(BasePage):
    def open(self):
        return self.open_route("product/search")

    def search(self, query):
        self.fill("#input-search", query)
        self.click("#button-search")

    def product_titles(self):
        self.wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, "#content .product-thumb"))
        return [e.text for e in self.driver.find_elements(
            By.CSS_SELECTOR, "#content .product-thumb .title a")]
