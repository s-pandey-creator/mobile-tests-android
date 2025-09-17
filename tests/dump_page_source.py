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

BS_APP_ID = "bs://06cff65c394b08d3fd0b3e93bfb23d612589f234"
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
    "appium:app": BS_APP_ID,
    "bstack:options": bstack_options
}

if AppiumOptions is not None:
    options = AppiumOptions()
    options.load_capabilities(caps)
    driver = webdriver.Remote("http://hub-cloud.browserstack.com/wd/hub", options=options)
else:
    driver = webdriver.Remote("http://hub-cloud.browserstack.com/wd/hub", caps)

try:
    time.sleep(4)
    xml = driver.page_source
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    out_dir = os.path.join(os.getcwd(), "artifacts")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"pagesource_android_{ts}.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)
    print("✅ Saved page source to:", path)
finally:
    try:
        driver.quit()
    except Exception:
        pass
