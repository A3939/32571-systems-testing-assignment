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
        checkbox = self.visible('input[name="agree"]')
        if not checkbox.is_selected():
            checkbox.click()

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
            if self.current_route() == "account/account":
                return "authenticated"
            alerts = driver.find_elements(By.CSS_SELECTOR, ".alert-danger")
            messages = [alert.text for alert in alerts if alert.is_displayed() and alert.text]
            return " | ".join(messages) if messages else False

        return self.wait.until(outcome, "Login produced neither an account page nor a visible error")


class AccountPage(BasePage):
    LOGOUT_LINK = 'a.list-group-item[href*="route=account/logout"]'

    def open(self):
        return self.open_route("account/account")

    def logout(self):
        self.click(self.LOGOUT_LINK)
