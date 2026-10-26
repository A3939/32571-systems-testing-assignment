from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class ProductPage(BasePage):
    def open(self, product_id):
        return self.open_route(f"product/product&product_id={product_id}")

    def name(self):
        return self.visible("#content h1").text.strip()

    def main_image_alt(self):
        return self.visible(".thumbnails > li:first-child img").get_attribute("alt")

    def price(self):
        return self.visible("#content h1 ~ ul.list-unstyled h2").text.strip()

    def availability(self):
        items = self.driver.find_elements(
            By.CSS_SELECTOR,
            "#content h1 + ul.list-unstyled li",
        )
        availability = next(
            item.text for item in items if item.text.startswith("Availability:")
        )
        return availability.split(":", 1)[1].strip()

    def option_label(self, selector):
        option = self.visible(selector)
        option_id = option.get_attribute("id")
        return self.visible(f'label[for="{option_id}"]').text.strip()

    def option_choices(self, selector):
        return [option.text.strip() for option in Select(self.visible(selector)).options]

    def select_option(self, selector, text):
        select = Select(self.visible(selector))
        select.select_by_visible_text(text)
        return select.first_selected_option.text.strip()
