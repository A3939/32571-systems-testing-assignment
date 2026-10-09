from urllib.parse import parse_qs, urlparse
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RegistrationPage(BasePage):
    def open(self):
        return self.open_route("account/register")

    def complete(self, email, password="Study!Pass123", confirm=None):
        values = {"firstname": "Study", "lastname": "Tester", "email": email,
                  "telephone": "0412345678", "password": password,
                  "confirm": password if confirm is None else confirm}
        for name, value in values.items():
            self.fill(f"#input-{name}", value)
        return self

    def accept_policy(self):
        # The native checkbox is styled/hidden; use its visible label.
        self.click('label[for="input-agree"]')

    def submit(self):
        self.click('#content input[type="submit"]')


class LoginPage(BasePage):
    def open(self):
        return self.open_route("account/login")

    def login(self, email, password):
        self.fill("#input-email", email)
        self.fill("#input-password", password)
        self.click('#content input[type="submit"]')

    def login_result(self):
        """Return a clear outcome without assuming a particular heading layout."""
        def outcome(driver):
            route = parse_qs(urlparse(driver.current_url).query).get("route", [""])[0]
            if route == "account/account":
                return "authenticated"
            alerts = driver.find_elements(By.CSS_SELECTOR, ".alert-danger")
            messages = [alert.text for alert in alerts if alert.is_displayed() and alert.text]
            return " | ".join(messages) if messages else False

        return self.wait.until(outcome, "Login produced neither an account page nor a visible error")
