import pytest
from pages.login_page import LoginPage

def test_locked_out_user_shows_error(driver):
    lp = LoginPage(driver)
    lp.login("locked_out_user", "secret_sauce")
    err = lp.get_error()
    assert err and len(err) > 0, "Locked out user should see an error"
