# conftest.py
import os
import pytest
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse, urlunparse

# Try modern AppiumOptions / UiAutomator2Options paths
AppiumOptions = None
UiAutomator2Options = None
try:
    from appium.options.common.base import AppiumOptions
except Exception:
    try:
        from appium.options.appium_options import AppiumOptions
    except Exception:
        AppiumOptions = None

try:
    from appium.options.android import UiAutomator2Options
except Exception:
    UiAutomator2Options = None


class DictOptions:
    """Minimal options-wrapper with to_capabilities() and _ignore_local_proxy."""
    def __init__(self, caps: dict):
        self._caps = dict(caps)
        self._ignore_local_proxy = False

    def to_capabilities(self):
        return dict(self._caps)


def _build_hub_url():
    """
    Return a hub URL with credentials embedded if not already present.
    Priority:
      1) BS_HUB env var (if contains credentials or https, used as-is)
      2) Build from username/key into https://username:key@hub-cloud.browserstack.com/wd/hub
    """
    hub = os.environ.get("BS_HUB", "https://hub-cloud.browserstack.com/wd/hub")
    # ensure https
    if hub.startswith("http://"):
        hub = "https://" + hub[len("http://"):]

    parsed = urlparse(hub)
    if parsed.username and parsed.password:
        return hub  # already has credentials
    user = os.environ.get("BROWSERSTACK_USER", os.environ.get("BS_USER"))
    key = os.environ.get("BROWSERSTACK_KEY", os.environ.get("BS_KEY"))
    if user and key and ("browserstack" in parsed.netloc):
        # inject credentials
        netloc = f"{user}:{key}@{parsed.netloc}"
        parsed = parsed._replace(netloc=netloc)
        return urlunparse(parsed)
    return hub


def create_remote(hub: str, caps: dict):
    """
    Create a webdriver.Remote session using the most compatible approach.
    Preferred order:
      1) UiAutomator2Options().load_capabilities(caps) -> options=
      2) AppiumOptions() with set_capability -> options=
      3) Fallback -> DictOptions(caps) -> options=
    """
    # 1) UiAutomator2Options path (Android-specific)
    if UiAutomator2Options is not None:
        try:
            opts = UiAutomator2Options().load_capabilities(caps)
            return webdriver.Remote(command_executor=hub, options=opts)
        except Exception:
            pass

    # 2) Generic AppiumOptions path
    if AppiumOptions is not None:
        try:
            opts = AppiumOptions()
            for k, v in caps.items():
                try:
                    opts.set_capability(k, v)
                except Exception:
                    try:
                        opts[k] = v
                    except Exception:
                        pass
            return webdriver.Remote(command_executor=hub, options=opts)
        except Exception:
            pass

    # 3) Fallback: use DictOptions which implements to_capabilities() & _ignore_local_proxy
    opts = DictOptions(caps)
    return webdriver.Remote(command_executor=hub, options=opts)


@pytest.fixture(scope="function")
def driver(request):
    """Fixture to create and tear down a BrowserStack Appium driver."""
    hub = _build_hub_url()
    platform = os.environ.get("PLATFORM", "android").lower()

    user = os.environ.get("BROWSERSTACK_USER", "sandeep_y6l5vm")
    key = os.environ.get("BROWSERSTACK_KEY", "9WrWAvFqpmhBcJggzJzy")
    app_id = os.environ.get("BROWSERSTACK_APP", "bs://06cff65c394b08d3fd0b3e93bfb23d612589f234")

    caps = {
        "platformName": "Android" if platform == "android" else "iOS",
        "deviceName": os.environ.get("BS_DEVICE", "Samsung Galaxy S22" if platform == "android" else "iPhone 14"),
        "platformVersion": os.environ.get("BS_PLATFORM_VERSION", "12.0" if platform == "android" else "16"),
        "app": app_id,
        "automationName": "UiAutomator2" if platform == "android" else "XCUITest",
        "browserstack.user": user,
        "browserstack.key": key,
        "project": "Mobile Demo",
        "build": f"{platform.capitalize()} Build",
        "name": request.node.name,
    }

    drv = create_remote(hub, caps)
    yield drv
    try:
        drv.quit()
    except Exception:
        pass


@pytest.fixture(scope="function")
def wait(driver):
    """Fixture to provide WebDriverWait for convenience in tests."""
    return WebDriverWait(driver, 10)
