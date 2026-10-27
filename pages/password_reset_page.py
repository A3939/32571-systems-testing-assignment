from pages.base_page import BasePage


class PasswordResetPage(BasePage):
    CONFIRMATION = "An email with a confirmation link has been sent your email address."
    UNKNOWN_EMAIL = "The E-Mail Address was not found in our records, please try again!"

    def open(self):
        return self.open_route("account/forgotten")

    def request_reset(self, email):
        self.fill("#input-email", email)
        self.click('#content input[type="submit"]')
