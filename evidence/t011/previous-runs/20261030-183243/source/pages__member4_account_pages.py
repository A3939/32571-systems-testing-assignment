"""Page objects for Member 4: wish list (F07), edit account (F11), address book (F12)."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ProductWishPage(BasePage):
    """Product page with the 'Add to Wish List' button (from F04 product details)."""
    WISH_BUTTON = '#content button[onclick^="wishlist.add"]'

    def open(self, product_id):
        return self.open_route(f"product/product&product_id={product_id}")

    def product_name(self):
        return self.visible("#content h1").text.strip()

    def add_to_wishlist(self):
        self.click(self.WISH_BUTTON)
        return self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        ).text.replace("×", "").strip()

    def header_wishlist_total(self):
        return self.visible("#wishlist-total").text.strip()

    def wait_header_wishlist_total(self, text):
        self.expect_text("#wishlist-total", text)


class WishListPage(BasePage):
    ROWS = "#content table tbody tr"

    def open(self):
        return self.open_route("account/wishlist")

    def product_names(self):
        if self.current_route() != "account/wishlist":
            return []
        return [row.find_element(By.CSS_SELECTOR, "td:nth-child(2) a").text.strip()
                for row in self.driver.find_elements(By.CSS_SELECTOR, self.ROWS)]

    def row(self, name):
        for row in self.driver.find_elements(By.CSS_SELECTOR, self.ROWS):
            if row.find_element(By.CSS_SELECTOR, "td:nth-child(2) a").text.strip() == name:
                cells = row.find_elements(By.CSS_SELECTOR, "td")
                return {"product": cells[1].text.strip(), "model": cells[2].text.strip(),
                        "stock": cells[3].text.strip(), "price": cells[4].text.strip(), "element": row}
        raise AssertionError(f"{name} is not on the wish list")

    def remove(self, name):
        self.row(name)["element"].find_element(By.CSS_SELECTOR, 'a[href*="remove="]').click()

    def success_alert(self):
        return self.visible(".alert-success").text.replace("×", "").strip()

    def content_text(self):
        return self.visible("#content").text


class AccountMenu(BasePage):
    def open(self):
        return self.open_route("account/account")

    def go_to(self, link_text):
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, link_text))).click()

    def success_alert(self):
        return self.visible(".alert-success").text.replace("×", "").strip()


class EditAccountPage(BasePage):
    FIELDS = ("firstname", "lastname", "email", "telephone")

    def open(self):
        return self.open_route("account/edit")

    def values(self):
        return {name: self.visible(f"#input-{name}").get_attribute("value") for name in self.FIELDS}

    def update(self, **values):
        for name, value in values.items():
            self.fill(f"#input-{name}", value)
        self.click('#content input[type="submit"]')

    def field_errors(self):
        """Map each field to its inline validation message (OpenCart .text-danger)."""
        errors = {}
        for name in self.FIELDS:
            messages = self.driver.find_elements(By.CSS_SELECTOR, f"#input-{name} ~ .text-danger")
            text = " ".join(m.text.strip() for m in messages if m.text.strip())
            if text:
                errors[name] = text
        return errors

    def wait_for_errors(self):
        return self.wait.until(lambda d: self.field_errors() or False, "No field validation message appeared")


class AddressBookPage(BasePage):
    ENTRIES = "#content table tbody tr"

    def open(self):
        return self.open_route("account/address")

    def entries(self):
        return [row.find_element(By.CSS_SELECTOR, "td.text-left").text.strip()
                for row in self.driver.find_elements(By.CSS_SELECTOR, self.ENTRIES)]

    def entry_row(self, contains):
        for row in self.driver.find_elements(By.CSS_SELECTOR, self.ENTRIES):
            if contains in row.text:
                return row
        raise AssertionError(f"No address entry contains {contains!r}")

    def click_new(self):
        self.click('#content a[href*="route=account/address/add"]')

    def click_edit(self, contains):
        self.entry_row(contains).find_element(By.CSS_SELECTOR, 'a[href*="route=account/address/edit"]').click()

    def click_delete(self, contains):
        self.entry_row(contains).find_element(By.CSS_SELECTOR, 'a[href*="route=account/address/delete"]').click()

    def alert(self, kind="success"):
        return self.visible(f".alert-{kind}").text.replace("×", "").strip()

    def content_text(self):
        return self.visible("#content").text


class AddressFormPage(BasePage):
    TEXT_FIELDS = ("firstname", "lastname", "company", "address-1", "address-2", "city", "postcode")

    def open_new(self):
        return self.open_route("account/address/add")

    def fill_address(self, country=None, zone=None, **values):
        for name, value in values.items():
            self.fill(f"#input-{name.replace('_', '-')}", value)
        if country:
            self._select_country(country)
        if zone:
            self.wait.until(lambda d: any(o.text.strip() == zone for o in Select(
                d.find_element(By.ID, "input-zone")).options), f"Region {zone} was not loaded")
            Select(self.visible("#input-zone")).select_by_visible_text(zone)

    def _select_country(self, country):
        select = self.visible("#input-country")
        self.wait.until(lambda d: select.is_enabled())
        Select(select).select_by_visible_text(country)
        # The region list reloads by AJAX; wait until the country list is re-enabled and regions exist.
        self.wait.until(lambda d: d.find_element(By.ID, "input-country").is_enabled()
                        and len(Select(d.find_element(By.ID, "input-zone")).options) > 1)

    def set_default(self, default):
        self.click(f'input[name="default"][value="{1 if default else 0}"]')

    def submit(self):
        self.click('#content input[type="submit"]')

    def field_errors(self):
        errors = {}
        for field in self.driver.find_elements(By.CSS_SELECTOR, "#content .form-group"):
            messages = [m.text.strip() for m in field.find_elements(By.CSS_SELECTOR, ".text-danger") if m.text.strip()]
            if messages:
                label = field.find_element(By.CSS_SELECTOR, "label").text.strip()
                errors[label] = " ".join(messages)
        return errors

    def wait_for_errors(self):
        return self.wait.until(lambda d: self.field_errors() or False, "No field validation message appeared")

    def value(self, name):
        return self.visible(f"#input-{name}").get_attribute("value")
