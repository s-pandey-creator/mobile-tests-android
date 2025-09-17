# pages/product_page.py
import re
import os
from datetime import datetime
from xml.etree import ElementTree as ET

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

class ProductPage:
    def __init__(self, driver, wait=None, timeout: int = 10):
        self.driver = driver
        if wait is not None and hasattr(wait, "until"):
            self.wait = wait
        else:
            self.wait = WebDriverWait(driver, float(timeout))

        caps = getattr(driver, "capabilities", {}) or getattr(driver, "desired_capabilities", {}) or {}
        self.platform = (caps.get("platformName") or "").lower()

        self._products_header_candidates = [
            (AppiumBy.ACCESSIBILITY_ID, "test-PRODUCTS"),
            (AppiumBy.ACCESSIBILITY_ID, "Products"),
            (AppiumBy.XPATH, "//android.widget.TextView[@text='Products']"),
        ]
        self._first_title_candidates = [
            (AppiumBy.ACCESSIBILITY_ID, "test-Item title"),
            (AppiumBy.ID, "com.sauce.demo:id/product_name"),
            (AppiumBy.XPATH, "(//android.widget.TextView[contains(@resource-id,'title')])[1]"),
        ]
        self._price_candidates = [
            (AppiumBy.ACCESSIBILITY_ID, "test-Price"),
            (AppiumBy.ID, "com.sauce.demo:id/product_price"),
            (AppiumBy.XPATH, "//android.widget.TextView[contains(@text,'$') or contains(@text,'₹')]"),
        ]
        self._detail_title_candidates = [
            (AppiumBy.ACCESSIBILITY_ID, "test-Item title"),
            (AppiumBy.ID, "com.sauce.demo:id/product_detail_name"),
            (AppiumBy.XPATH, "//android.widget.TextView[contains(@resource-id,'detail_title')]"),
        ]
        self._detail_price_candidates = [
            (AppiumBy.ACCESSIBILITY_ID, "test-Price"),
            (AppiumBy.ID, "com.sauce.demo:id/product_detail_price"),
            (AppiumBy.XPATH, "//android.widget.TextView[contains(@text,'$') or contains(@text,'₹')]"),
        ]

    def find(self, locator, timeout=5):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        except Exception:
            return None

    def products_header(self):
        return self._products_header_candidates[0]

    def get_first_product_title_text(self) -> str:
        for loc in self._first_title_candidates:
            el = self.find(loc, timeout=2)
            if el:
                return (el.text or "").strip()
        return ""

    def get_first_product_price_text(self) -> str:
        for loc in self._price_candidates:
            els = self.driver.find_elements(*loc)
            if els:
                return (els[0].text or "").strip()
        return ""

    def open_first_product(self) -> bool:
        try:
            el = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Item title")
            el.click()
            return True
        except Exception:
            return False

    def get_detail_title_text(self) -> str:
        for loc in self._detail_title_candidates:
            el = self.find(loc, timeout=3)
            if el:
                return (el.text or "").strip()
        return ""

    def get_detail_price_text(self) -> str:
        for loc in self._detail_price_candidates:
            el = self.find(loc, timeout=3)
            if el:
                return (el.text or "").strip()
        return ""

    def detail_contains_price(self, price_str: str, timeout: int = 2) -> bool:
        """Check if given price string appears on detail screen."""
        if not price_str:
            return False
        try:
            raw = self.driver.page_source or ""
            if price_str in raw:
                return True
        except Exception:
            pass
        return False

    def get_visible_prices(self):
        prices = []
        for loc in self._price_candidates:
            els = self.driver.find_elements(*loc)
            for e in els:
                txt = (e.text or "").strip()
                if txt:
                    try:
                        val = float(re.sub(r"[^\d.]", "", txt))
                        prices.append(val)
                    except Exception:
                        continue
        return prices
