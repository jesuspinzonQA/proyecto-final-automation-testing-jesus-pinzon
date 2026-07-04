from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CartPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def wait_until_loaded(self):
        self.wait.until(EC.url_contains("/cart.html"))
        self.find_visible(self.TITLE)

    def get_item_names(self):
        return [element.text for element in self.find_all_visible(self.ITEM_NAMES)]

    def get_item_count(self):
        return len(self.find_all_visible(self.CART_ITEMS))

    def start_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
