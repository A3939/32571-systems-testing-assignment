from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    BILLING = "#collapse-payment-address"
    DELIVERY_METHOD = "#collapse-shipping-method"
    BLANK_GUEST_ERRORS = {
        "firstname": "First Name must be between 1 and 32 characters!",
        "lastname": "Last Name must be between 1 and 32 characters!",
        "email": "E-Mail address does not appear to be valid!",
        "telephone": "Telephone must be between 3 and 32 characters!",
        "address-1": "Address 1 must be between 3 and 128 characters!",
        "city": "City must be between 2 and 128 characters!",
        "postcode": "Postcode must be between 2 and 10 characters!",
        "zone": "Please select a region / state!",
    }

    def open(self):
        return self.open_route("checkout/checkout")

    def continue_as_guest(self):
        self.click("#collapse-checkout-option input[name='account'][value='guest']")
        self.click("#button-account")
        self.visible("#input-payment-firstname")
        # The form loads regions for the default country and disables the country list until they arrive.
        self.wait_for_ajax()

    def fill_guest_details(self, details):
        """Fill Step 2 text fields; `country` and `zone` are chosen by visible text."""
        details = dict(details)
        country, zone = details.pop("country"), details.pop("zone")
        for field, value in details.items():
            self.fill(f"#input-payment-{field}", value)
        Select(self.visible("#input-payment-country")).select_by_visible_text(country)
        # Regions are reloaded by AJAX after the country changes.
        self.wait.until(lambda driver: any(option.text.strip() == zone for option in
                                           driver.find_elements(By.CSS_SELECTOR, "#input-payment-zone option")))
        Select(self.visible("#input-payment-zone")).select_by_visible_text(zone)

    def submit_guest_details(self):
        previous = self.driver.find_elements(By.CSS_SELECTOR, f"{self.BILLING} .text-danger")
        self.click("#button-guest")
        # Earlier messages are removed only when the validation response arrives.
        for element in previous:
            self.wait.until(EC.staleness_of(element))

    def field_errors(self):
        """Wait for Step 2 validation and map each field (id without `input-payment-`) to its message."""
        def collect(driver):
            errors = {}
            for message in driver.find_elements(By.CSS_SELECTOR, f"{self.BILLING} .text-danger"):
                if message.is_displayed():
                    field = message.find_element(By.XPATH, "preceding-sibling::*[1]").get_attribute("id")
                    errors[field.removeprefix("input-payment-")] = message.text.strip()
            return errors or False

        return self.wait.until(collect, "Step 2 showed no field validation messages")

    def visible_field_errors(self):
        return [message.text for message in self.driver.find_elements(By.CSS_SELECTOR, f"{self.BILLING} .text-danger")
                if message.is_displayed()]

    def open_steps(self):
        self.wait.until(lambda driver: not driver.find_elements(By.CSS_SELECTOR, ".panel-collapse.collapsing"))
        return [panel.get_attribute("id") for panel in self.driver.find_elements(By.CSS_SELECTOR, ".panel-collapse.in")]
