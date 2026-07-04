from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    APP_LOGO = (By.CLASS_NAME, "app_logo")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")

    def wait_until_loaded(self):
        self.wait.until(EC.url_contains("/inventory.html"))
        self.find_visible(self.TITLE)

    def get_title(self):
        return self.get_text(self.TITLE)

    def get_logo(self):
        return self.get_text(self.APP_LOGO)

    def get_product_count(self):
        return len(self.find_all_visible(self.INVENTORY_ITEMS))

    def get_product_names(self):
        return [element.text for element in self.find_all_visible(self.PRODUCT_NAMES)]

    def has_main_controls(self):
        return all(
            [
                self.find_visible(self.MENU_BUTTON).is_displayed(),
                self.find_visible(self.SORT_SELECT).is_displayed(),
                self.find_visible(self.CART_LINK).is_displayed(),
            ]
        )

    def sort_by(self, visible_text):
        Select(self.find_visible(self.SORT_SELECT)).select_by_visible_text(visible_text)

    def add_product_by_name(self, product_name):
        product_xpath = (
            "//div[contains(@class, 'inventory_item')][.//div[text()="
            f"{product_name!r}]]//button"
        )
        self.click((By.XPATH, product_xpath))

    def get_cart_badge_count(self):
        return self.get_text(self.CART_BADGE)

    def open_cart(self):
        self.click(self.CART_LINK)
