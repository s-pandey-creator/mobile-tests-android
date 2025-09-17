# pages/sort_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
from selenium.webdriver.common.by import By

class SortPage(BasePage):
    # open sort/filter modal: sample app uses menu button content-desc "test-Menu" then "Price (low to high)" list
    def open_sort_menu(self):
        try:
            self.click((AppiumBy.ACCESSIBILITY_ID, "test-Menu"))
        except Exception:
            # fallback: click any menu icon
            el = self.find((AppiumBy.XPATH, "//*[contains(@content-desc,'Menu') or contains(@resource-id,'menu') or @class='android.widget.ImageView']"), timeout=3)
            el.click()

    def sort_by(self, key):
        # key expects 'price_low_to_high' or 'price_high_to_low' etc.
        self.open_sort_menu()
        # sample app might show a modal with text like "Price (low to high)"
        mapping = {
            "price_low_to_high": "Price (low to high)",
            "price_high_to_low": "Price (high to low)",
            "name_az": "Name (A to Z)",
            "name_za": "Name (Z to A)"
        }
        txt = mapping.get(key, key)
        # try to click by exact text
        try:
            self.click((AppiumBy.XPATH, f"//android.widget.TextView[@text='{txt}' or contains(@text,'{txt}')]"), timeout=5)
        except Exception:
            # last fallback: click first option
            opts = self.find_all((AppiumBy.XPATH, "//android.widget.TextView"), timeout=3)
            if opts:
                opts[0].click()
