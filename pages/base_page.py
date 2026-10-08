from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, 15)

    def open_route(self, route):
        self.driver.get(f"{self.base_url}/index.php?route={route}")
        return self

    def visible(self, selector):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def fill(self, selector, value):
        field = self.visible(selector)
        field.clear()
        field.send_keys(value)

    def click(self, selector):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()

    def expect_text(self, selector, text):
        self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text))
