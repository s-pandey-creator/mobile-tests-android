# tests/test_products.py
import re
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductPage

def parse_price(s: str) -> float | None:
    if not s:
        return None
    s = s.strip()
    s = re.sub(r'[^\d\.,]', '', s)
    if not s:
        return None
    if ',' in s and '.' in s:
        s = s.replace(',', '')
    elif ',' in s and '.' not in s:
        s = s.replace(',', '.')
    try:
        return float(s)
    except Exception:
        try:
            return float(s.replace(',', ''))
        except Exception:
            return None

@pytest.mark.smoke
def test_open_product_and_verify(driver):
    lp = LoginPage(driver)
    lp.login("standard_user", "secret_sauce")
    assert lp.is_logged_in()

    pp = ProductPage(driver)
    assert pp.find(pp.products_header()), "Products header not found"

    title = pp.get_first_product_title_text()
    price_list = pp.get_first_product_price_text()
    assert title, "Could not read first product title"
    assert price_list, "Could not read first product price"

    opened = pp.open_first_product()
    assert opened, "Could not open product details"

    detail_title = pp.get_detail_title_text()
    detail_price = pp.get_detail_price_text()
    assert detail_title, "Could not read product detail title"
    assert detail_price is not None, "Could not read product detail price"

    p_list_num = parse_price(price_list)
    p_detail_num = parse_price(detail_price)

    assert p_list_num is not None, f"Failed to parse list price '{price_list}'"
    assert p_detail_num is not None, f"Failed to parse detail price '{detail_price}'"

    assert abs(p_list_num - p_detail_num) < 0.01, f"Price mismatch: list='{price_list}' detail='{detail_price}'"
    assert title == detail_title, f"Title mismatch: list='{title}' detail='{detail_title}'"
