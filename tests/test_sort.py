# tests/test_sort.py
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductPage

@pytest.mark.smoke
def test_sort_by_price(driver, wait):
    lp = LoginPage(driver, wait)
    lp.login("standard_user", "secret_sauce")
    assert lp.is_logged_in()

    pp = ProductPage(driver, wait)
    prices_before = pp.get_visible_prices()
    assert prices_before, "Could not read visible prices before sort"

    # apply sort via UI - your app likely has a sort control; try to call it:
    # Try several common locators / flows. If your app uses a known control, replace below.
    try:
        # example: open sort dropdown and choose 'Price (low to high)'
        sort_btn = driver.find_element_by_accessibility_id("test-Modal Selector")
        sort_btn.click()
    except Exception:
        pass

    # If your app exposes a select, tests may need to choose the option.
    # We will wait a short time and then read prices again.
    import time
    time.sleep(1)
    prices_after = pp.get_visible_prices()
    assert prices_after, "Could not read visible prices after sort"

    # verify ascending order
    assert prices_after == sorted(prices_after), f"Prices not sorted ascending: before={prices_before} after={prices_after}"
