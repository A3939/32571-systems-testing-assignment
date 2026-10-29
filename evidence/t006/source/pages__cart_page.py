from collections import namedtuple

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage

CatalogueProduct = namedtuple("CatalogueProduct", "product_id name price")

# Live-site stock at design time (29 Oct 2026): iPod Classic 528, Canon EOS 5D 20.
IPOD_CLASSIC = CatalogueProduct(48, "iPod Classic", "$122.00")
CANON_EOS_5D = CatalogueProduct(30, "Canon EOS 5D", "$98.00")


def added_message(product):
    return f"Success: You have added {product.name} to your shopping cart!"


class ProductPurchasePage(BasePage):
    """Quantity, options and Add to Cart button on a product page."""

    def open(self, product_id):
        return self.open_route(f"product/product&product_id={product_id}")

    def name(self):
        return self.visible("#content h1").text.strip()

    def set_quantity(self, quantity):
        self.fill("#input-quantity", str(quantity))
        self.visible("#input-quantity").send_keys(Keys.TAB)
        # Leaving the field fires getRecurringDescription, whose response removes every alert on the
        # page. If it lands after the add-to-cart response, the success alert vanishes (seen live).
        self.wait_for_ajax()

    def select_option(self, label, choice):
        labels = self.driver.find_elements(By.CSS_SELECTOR, "#product label.control-label")
        target = next(item.get_attribute("for") for item in labels if item.text.strip() == label)
        Select(self.visible(f"#{target}")).select_by_visible_text(choice)

    def add_to_cart(self):
        """Return the success alert or validation error produced by the AJAX request."""
        previous = self.driver.find_elements(By.CSS_SELECTOR, ".alert, #product .text-danger")
        self.click("#button-cart")
        # The page clears earlier messages only when the response arrives.
        for element in previous:
            self.wait.until(EC.staleness_of(element))

        def outcome(driver):
            for selector in (".alert-success", "#product .text-danger"):
                shown = [e.text.replace("×", "").strip() for e in driver.find_elements(By.CSS_SELECTOR, selector)
                         if e.is_displayed()]
                if shown:
                    return " | ".join(shown)
            return False

        return self.wait.until(outcome, "Add to Cart showed neither a success alert nor a validation error")


class CartPage(BasePage):
    EMPTY = "Your shopping cart is empty!"
    MODIFIED = "Success: You have modified your shopping cart!"
    STOCK_WARNING = "Products marked with *** are not available in the desired quantity or not in stock!"
    ROWS = "#content form table tbody tr"

    def open(self):
        return self.open_route("checkout/cart")

    def rows(self):
        """Map each product name to the quantity, option details and line total shown in the cart."""
        result = {}
        for row in self.driver.find_elements(By.CSS_SELECTOR, self.ROWS):
            cells = row.find_elements(By.TAG_NAME, "td")
            name = cells[1].find_element(By.TAG_NAME, "a").text.strip()
            result[name] = {
                "details": cells[1].text.strip(),
                "quantity": cells[3].find_element(By.CSS_SELECTOR, "input").get_attribute("value"),
                "unit_price": cells[4].text.strip(),
                "total": cells[5].text.strip(),
            }
        return result

    def totals(self):
        result = {}
        for row in self.driver.find_elements(By.CSS_SELECTOR, "#content .col-sm-4 table tr"):
            label, amount = (cell.text.strip() for cell in row.find_elements(By.TAG_NAME, "td"))
            result[label.rstrip(":")] = amount
        return result

    def has_stock_warning(self):
        return any(alert.is_displayed() and self.STOCK_WARNING in alert.text
                   for alert in self.driver.find_elements(By.CSS_SELECTOR, ".alert-danger"))

    def _row(self, product_name):
        return self.visible_xpath(f"//*[@id='content']//form//tbody/tr[td[2]/a[normalize-space()='{product_name}']]")

    def visible_xpath(self, xpath):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def update_quantity(self, product_name, quantity):
        row = self._row(product_name)
        field = row.find_element(By.CSS_SELECTOR, "input[name^='quantity']")
        field.clear()
        field.send_keys(str(quantity))
        row.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait.until(EC.staleness_of(row))

    def remove(self, product_name):
        row = self._row(product_name)
        row.find_element(By.CSS_SELECTOR, "button.btn-danger").click()
        # The remove request reloads checkout/cart when it completes.
        self.wait.until(EC.staleness_of(row))
        self.visible("#content h1")
