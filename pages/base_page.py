from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Clase base para centralizar esperas e interacciones comunes."""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)

    def find_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def find_all_visible(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator):
        self.find_clickable(locator).click()

    def type_text(self, locator, text):
        element = self.find_visible(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_visible(locator).text
