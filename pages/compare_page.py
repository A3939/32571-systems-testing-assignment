from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ComparePage(BasePage):
    def open(self):
        return self.open_route("product/compare")

    def row_values(self, label):
        rows = self.wait.until(
            lambda driver: driver.find_elements(
                By.CSS_SELECTOR,
                "#content table.table-bordered tbody tr",
            )
        )
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and cells[0].text.strip() == label:
                return [cell.text.strip() for cell in cells[1:]]
        raise AssertionError(f"Comparison row not found: {label}")

    def product_names(self):
        return self.row_values("Product")

    def prices(self):
        return self.row_values("Price")

    def models(self):
        return self.row_values("Model")

    def brands(self):
        return self.row_values("Brands")

    def availability(self):
        return self.row_values("Availability")
