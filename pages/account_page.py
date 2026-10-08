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
