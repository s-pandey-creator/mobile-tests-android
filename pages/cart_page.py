# pages/cart_page.py
import os
from datetime import datetime
from xml.etree import ElementTree as ET

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

class CartPage:
    def __init__(self, driver, wait=None, timeout: int = 10):
        self.driver = driver
        if wait is not None and hasattr(wait, "until"):
            self.wait = wait
        else:
            try:
                numeric_timeout = float(wait) if wait is not None else float(timeout)
            except Exception:
                numeric_timeout = float(timeout)
            self.wait = WebDriverWait(driver, numeric_timeout)

        # locators (update if your app differs)
        self.add_to_cart_button_candidates = [
            (AppiumBy.ACCESSIBILITY_ID, "test-ADD TO CART"),
            (AppiumBy.XPATH, "//android.widget.Button[contains(@text,'ADD TO CART') or contains(@content-desc,'add')]"),
        ]
        self.cart_icon_candidates = [
            (AppiumBy.ACCESSIBILITY_ID, "test-Cart"),
            (AppiumBy.ID, "com.sauce.demo:id/cart")
        ]
        self.cart_item_name_candidates = [
            (AppiumBy.XPATH, "//android.widget.TextView[contains(@resource-id,'cart_item') or contains(@text,'')]"),
            (AppiumBy.ID, "com.sauce.demo:id/cart_item_name")
        ]

    def add_first_product_to_cart(self):
        # Try to click an 'Add to cart' for the first visible product
        for loc in self.add_to_cart_button_candidates:
            try:
                els = self.driver.find_elements(*loc)
            except Exception:
                els = []
            if els:
                try:
                    els[0].click()
                    return True
                except Exception:
                    try:
                        rect = els[0].rect
                        cx = rect["x"] + rect["width"] / 2
                        cy = rect["y"] + rect["height"] / 2
                        self.driver.execute_script("mobile: tap", {"x": cx, "y": cy})
                        return True
                    except Exception:
                        continue
        return False

    def open_cart(self):
        for loc in self.cart_icon_candidates:
            el = None
            try:
                el = self.driver.find_element(*loc)
            except Exception:
                el = None
            if el:
                try:
                    el.click()
                    return True
                except Exception:
                    continue
        return False

    def get_cart_item_names(self):
        names = []
        for loc in self.cart_item_name_candidates:
            try:
                els = self.driver.find_elements(*loc)
            except Exception:
                els = []
            for e in els:
                t = (e.text or "").strip()
                if t:
                    names.append(t)
                else:
                    try:
                        t = e.get_attribute("content-desc") or e.get_attribute("name") or ""
                        if t:
                            names.append(t.strip())
                    except Exception:
                        continue
        return names

    def is_item_in_cart(self, name):
        names = self.get_cart_item_names()
        for n in names:
            if name.strip().lower() in n.strip().lower():
                return True
        return False
