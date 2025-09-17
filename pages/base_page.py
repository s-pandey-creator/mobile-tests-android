# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        # platform_name from driver set in conftest
        self.platform = getattr(driver, "platform_name", "android")

    def find(self, locator, timeout=None):
        w = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return w.until(EC.presence_of_element_located(locator))

    def click(self, locator, timeout=None):
        el = self.find(locator, timeout)
        el.click()
        return el

    def type(self, locator, text, timeout=None):
        el = self.find(locator, timeout)
        el.clear()
        el.send_keys(text)
        return el

    def find_all(self, locator, timeout=5):
        try:
            w = WebDriverWait(self.driver, timeout)
            return w.until(lambda d: d.find_elements(*locator))
        except TimeoutException:
            return []

    # helper: accessibility id locator
    def aid(self, id_value):
        return (AppiumBy.ACCESSIBILITY_ID, id_value)
