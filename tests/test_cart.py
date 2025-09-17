# tests/test_cart.py
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductPage
from pages.cart_page import CartPage

@pytest.mark.smoke
def test_add_to_cart(driver, wait):
    lp = LoginPage(driver, wait)
    lp.login("standard_user", "secret_sauce")
    assert lp.is_logged_in()

    pp = ProductPage(driver, wait)
    title = pp.get_first_product_title_text()
    assert title, "Could not read product title from list"

    cp = CartPage(driver, wait)
    added = cp.add_first_product_to_cart()
    assert added, "Failed to click Add to cart"

    opened = cp.open_cart()
    assert opened, "Failed to open cart"

    assert cp.is_item_in_cart(title), f"Item '{title}' not found in cart"
