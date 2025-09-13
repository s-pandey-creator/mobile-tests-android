import os
import pytest
from appium import webdriver

BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY")
ANDROID_APP = os.environ.get("ANDROID_APP")  # bs://...

@pytest.fixture(scope="function")
def driver(request):
    caps = {
        "platformName": "Android",
        "deviceName": "Google Pixel 5",
        "platformVersion": "13.0",
        "automationName": "UiAutomator2",
        "app": ANDROID_APP,
        "project": "Demo POM Android",
        "build": "android-build-1",
        "name": request.node.name,
        "browserstack.debug": True,
        "browserstack.networkLogs": True
    }

    hub = f"http://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"
    driver = webdriver.Remote(hub, caps)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
