# tests/check_bs_connectivity.py
import os
import traceback
from appium import webdriver

# Try to import AppiumOptions from several known locations
AppiumOptions = None
_import_paths_tried = []

try:
    from appium.webdriver.common.appium_options import AppiumOptions  # newer path in some distros
    _import_paths_tried.append("appium.webdriver.common.appium_options")
except Exception as e:
    _import_paths_tried.append(f"appium.webdriver.common.appium_options -> {e}")

if AppiumOptions is None:
    try:
        from appium.options import AppiumOptions  # alternate path used by some releases
        _import_paths_tried.append("appium.options")
    except Exception as e:
        _import_paths_tried.append(f"appium.options -> {e}")

if AppiumOptions is None:
    try:
        # fallback: older clients may not provide AppiumOptions; we'll use dict capabilities instead
        AppiumOptions = None
        _import_paths_tried.append("no AppiumOptions available; will use dict caps fallback")
    except Exception as e:
        _import_paths_tried.append(f"fallback import error -> {e}")

BS_USER = os.getenv("BROWSERSTACK_USERNAME")
BS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")
APP_ID = os.getenv("ANDROID_APP_ID") or os.getenv("IOS_APP_ID") or ""

if not BS_USER or not BS_KEY:
    raise RuntimeError("Set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY in this session.")

def _bstack_options():
    return {"userName": BS_USER, "accessKey": BS_KEY, "projectName": "connectivity-check"}

def run():
    try:
        if AppiumOptions is not None:
            opts = AppiumOptions()
            # choose Android by default for connectivity
            opts.set_capability("platformName", "Android")
            opts.set_capability("automationName", "UiAutomator2")
            opts.set_capability("deviceName", "Google Pixel 7")
            opts.set_capability("platformVersion", "13.0")
            opts.set_capability("app", APP_ID)
            opts.set_capability("bstack:options", _bstack_options())
            opts.set_capability("newCommandTimeout", 60)

            driver = webdriver.Remote("https://hub.browserstack.com/wd/hub", options=opts)
        else:
            # dict fallback — may fail on some client versions, but we try
            caps = {
                "platformName": "Android",
                "automationName": "UiAutomator2",
                "deviceName": "Google Pixel 7",
                "platformVersion": "13.0",
                "app": APP_ID,
                "bstack:options": _bstack_options(),
                "newCommandTimeout": 60,
            }
            # try using appium.webdriver.Remote positional/keyword forms
            try:
                from appium import webdriver as _app_wd
                driver = _app_wd.Remote("https://hub.browserstack.com/wd/hub", caps)
            except Exception:
                # last resort: selenium remote
                from selenium import webdriver as _sel_wd
                driver = _sel_wd.Remote(command_executor="https://hub.browserstack.com/wd/hub", desired_capabilities=caps)

        print("Session started. session_id=", getattr(driver, "session_id", None))
        print("Capabilities:", getattr(driver, "capabilities", None))
        driver.quit()
    except Exception:
        print("CONNECTIVITY ERROR:")
        traceback.print_exc()
        print("\nImport attempts (for AppiumOptions):")
        for s in _import_paths_tried:
            print(" -", s)

if __name__ == "__main__":
    run()
