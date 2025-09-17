import os
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PLATFORM = os.environ.get('TEST_PLATFORM','android').lower()

class LoginPage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    _locators = {
        'username': {
            'android': (AppiumBy.ID, 'com.example.android:id/username'),
            'ios':     (AppiumBy.ACCESSIBILITY_ID, 'test-Username')
        },
        'password': {
            'android': (AppiumBy.ID, 'com.example.android:id/password'),
            'ios':     (AppiumBy.ACCESSIBILITY_ID, 'test-Password')
        },
        'login_btn': {
            'android': (AppiumBy.ACCESSIBILITY_ID, 'test-LOGIN'),
            'ios':     (AppiumBy.ACCESSIBILITY_ID, 'test-LOGIN')
        },
        'error': {
            'android': (AppiumBy.ID, 'com.example.android:id/error'),
            'ios':     (AppiumBy.ACCESSIBILITY_ID, 'test-Error')
        }
    }

    def _locator(self, name):
        entry = self._locators.get(name)
        if not entry:
            raise KeyError(f'No locator named: {name}')
        if PLATFORM in entry and entry[PLATFORM]:
            return entry[PLATFORM]
        return entry.get('android') or entry.get('ios')

    def enter_username(self, username):
        el = self.wait.until(EC.presence_of_element_located(self._locator('username')))
        el.clear()
        el.send_keys(username)

    def enter_password(self, password):
        el = self.wait.until(EC.presence_of_element_located(self._locator('password')))
        el.clear()
        el.send_keys(password)

    def tap_login(self):
        el = self.wait.until(EC.element_to_be_clickable(self._locator('login_btn')))
        el.click()

    def get_error(self):
        return self.wait.until(EC.visibility_of_element_located(self._locator('error'))).text
