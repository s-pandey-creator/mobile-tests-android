# tests/dump_page_source_bs_android.py
import os, time
from datetime import datetime
from appium import webdriver
try:
    from appium.options.common.base import AppiumOptions
except Exception:
    try:
        from appium.options.appium_options import AppiumOptions
    except Exception:
        AppiumOptions = None

BS_APP_ID = "bs://c80db3143136d8f81e97bec7327edd4957aaec8b"
BS_USER = "sandeeppandey_3z5YkG"
BS_KEY  = "7aU6Ny4pQdqVnJa8XxUw"

bstack_options = {
    "userName": BS_USER,
    "accessKey": BS_KEY,
    "deviceName": "Google Pixel 6",
    "osVersion": "13",
    "networkLogs": True
}

caps = {
    "platformName": "Android",
    "app": BS_APP_ID,
    "bstack:options": bstack_options
}

if AppiumOptions is not None:
    options = AppiumOptions()
    options.load_capabilities(caps)
    driver = webdriver.Remote("https://hub-cloud.browserstack.com/wd/hub", options=options)
else:
    driver = webdriver.Remote("https://hub-cloud.browserstack.com/wd/hub", desired_capabilities=caps)

time.sleep(4)
xml = driver.page_source
ts = datetime.now().strftime("%Y%m%dT%H%M%S")
out_dir = os.path.join(os.getcwd(), "artifacts")
os.makedirs(out_dir, exist_ok=True)
path = os.path.join(out_dir, f"pagesource_android_{ts}.xml")
with open(path, "w", encoding="utf-8") as f:
    f.write(xml)
print("Saved page source to:", path)
# take screenshot
screenshot_path = os.path.join(out_dir, f"screenshot_android_{ts}.png")
try:
    driver.save_screenshot(screenshot_path)
    print("Saved screenshot to:", screenshot_path)
except Exception as e:
    print("Failed to save screenshot:", e)
driver.quit()
