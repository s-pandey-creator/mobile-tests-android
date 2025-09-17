# pages/login_page.py
import os
from datetime import datetime
from xml.etree import ElementTree as ET

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

class LoginPage:
    """Robust login page object that works for Android and iOS sessions.

    Use: LoginPage(driver, wait) or LoginPage(driver, timeout=10)
    """

    def __init__(self, driver, wait=None, timeout: int = 10):
        self.driver = driver

        # accept a WebDriverWait instance or numeric timeout
        if wait is not None and hasattr(wait, "until"):
            self.wait = wait
        else:
            try:
                numeric_timeout = float(wait) if wait is not None else float(timeout)
            except Exception:
                numeric_timeout = float(timeout)
            self.wait = WebDriverWait(driver, numeric_timeout)

        # detect platform to avoid unsupported locator strategies
        caps = {}
        try:
            caps = getattr(driver, "capabilities", {}) or {}
            if not caps:
                caps = getattr(driver, "desired_capabilities", {}) or {}
        except Exception:
            caps = {}
        self.platform = (caps.get("platformName") or caps.get("platform") or "").lower()

        # --- Locators (prefer accessibility id / resource-id) ---
        self.username_locator = (AppiumBy.ACCESSIBILITY_ID, "test-Username")
        self.password_locator = (AppiumBy.ACCESSIBILITY_ID, "test-Password")
        self.login_button_locator = (AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")

        # Build post-login locators depending on platform
        post_login = [
            (AppiumBy.ACCESSIBILITY_ID, "test-PRODUCTS"),
            (AppiumBy.ACCESSIBILITY_ID, "Products"),
            (AppiumBy.XPATH, "//android.widget.TextView[@text='Products']"),
        ]
        if "ios" in self.platform:
            # only add IOS_PREDICATE if session is iOS
            post_login.append((AppiumBy.IOS_PREDICATE, "label == 'Products'"))
        self.post_login_locators = post_login

        # Error candidates (platform-appropriate)
        error_candidates = [
            (AppiumBy.ACCESSIBILITY_ID, "test-Error"),
            (AppiumBy.XPATH, "//*[contains(@text, 'Epic sadface')]"),
            (AppiumBy.XPATH, "//*[contains(@text, 'invalid')]"),
            # Common android toast variants (only useful on Android)
            (AppiumBy.XPATH, "//android.widget.Toast[1]"),
            (AppiumBy.XPATH, "//*[@class='android.widget.Toast']"),
        ]
        if "ios" in self.platform:
            error_candidates.append((AppiumBy.IOS_PREDICATE, "type == 'XCUIElementTypeAlert'"))
        self.error_locator_candidates = error_candidates

    # ---------------- actions / checks ----------------
    def login(self, username: str, password: str) -> None:
        el_user = self.wait.until(EC.presence_of_element_located(self.username_locator))
        el_user.clear()
        el_user.send_keys(username)

        el_pass = self.wait.until(EC.presence_of_element_located(self.password_locator))
        el_pass.clear()
        el_pass.send_keys(password)

        btn = self.wait.until(EC.element_to_be_clickable(self.login_button_locator))
        btn.click()

    def is_logged_in(self, timeout: int = 8) -> bool:
        """Return True if any post-login element is found within timeout."""
        wait = WebDriverWait(self.driver, timeout)
        for loc in self.post_login_locators:
            try:
                wait.until(EC.presence_of_element_located(loc))
                return True
            except TimeoutException:
                continue
            except Exception:
                continue
        return False

    def get_error_message(self, timeout: int = 5) -> str | None:
        """
        Robust error detection:
          1) Wait for common error locators (toast/label/alert)
          2) If nothing, search page_source for common keywords and try to extract nearby text
          3) Save diagnostics (page source + screenshot) when nothing is found
        Returns first discovered non-empty string or None.
        """
        wait = WebDriverWait(self.driver, timeout)

        # 1) Try explicit locators with short waits
        for loc in self.error_locator_candidates:
            # skip iOS locator on Android and vice-versa (safety)
            if loc[0] == AppiumBy.IOS_PREDICATE and "ios" not in self.platform:
                continue
            try:
                el = wait.until(EC.presence_of_element_located(loc))
                # extract text safely
                text = ""
                try:
                    text = el.text or ""
                except Exception:
                    try:
                        text = el.get_attribute("text") or el.get_attribute("name") or ""
                    except Exception:
                        text = ""
                text = (text or "").strip()
                if text:
                    return text
            except TimeoutException:
                continue
            except Exception:
                continue

        # 2) fallback: inspect page source for keywords
        try:
            raw = self.driver.page_source or ""
        except WebDriverException:
            raw = ""

        raw_lower = (raw or "").lower()
        keywords = ["epic sadface", "invalid", "wrong", "username", "password", "error", "failed", "credentials"]

        for kw in keywords:
            if kw in raw_lower:
                # try xml parse to find the node containing the keyword
                try:
                    root = ET.fromstring(raw)
                    for elem in root.iter():
                        combined = " ".join([
                            elem.attrib.get("text", ""),
                            elem.attrib.get("label", ""),
                            elem.attrib.get("content-desc", ""),
                            elem.attrib.get("resource-id", ""),
                            elem.attrib.get("value", ""),
                        ]).strip().lower()
                        if kw in combined:
                            candidate = (elem.attrib.get("text") or elem.attrib.get("label")
                                         or elem.attrib.get("content-desc") or combined)
                            if candidate:
                                return candidate.strip()
                except Exception:
                    # fallback to returning snippet of raw xml around first occurrence
                    idx = raw_lower.find(kw)
                    start = max(0, idx - 120)
                    end = min(len(raw_lower), idx + 180)
                    return raw[start:end].strip()

        # 3) nothing found: save diagnostics
        ts = datetime.now().strftime("%Y%m%dT%H%M%S")
        out_dir = os.path.join(os.getcwd(), "artifacts")
        os.makedirs(out_dir, exist_ok=True)

        ps_path = None
        ss_path = None
        try:
            ps_path = os.path.join(out_dir, f"pagesource_on_error_{ts}.xml")
            with open(ps_path, "w", encoding="utf-8") as f:
                f.write(raw)
        except Exception:
            ps_path = None

        try:
            ss_path = os.path.join(out_dir, f"screenshot_on_error_{ts}.png")
            self.driver.save_screenshot(ss_path)
        except Exception:
            ss_path = None

        # print minimal diagnostic so pytest output shows the files
        print(f"[LoginPage] No explicit error found. Saved diagnostics: pagesource={ps_path}, screenshot={ss_path}")

        return None

    def logout(self) -> None:
        """Try common logout flow (menu -> logout). Ignore errors if not present."""
        try:
            menu = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Menu")
            menu.click()
            logout_btn = self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "test-LOGOUT")))
            logout_btn.click()
        except (NoSuchElementException, TimeoutException, WebDriverException):
            return
