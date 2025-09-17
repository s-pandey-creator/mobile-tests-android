import pytest
from pages.login_page import LoginPage

@pytest.mark.smoke
class TestLogin:

    def test_valid_login(self, driver, wait):
        lp = LoginPage(driver, wait)
        lp.login("standard_user", "secret_sauce")
        assert lp.is_logged_in(), "Expected to be on products page after valid login"

    def test_invalid_login_shows_error(self, driver, wait):
        lp = LoginPage(driver, wait)
        lp.login("wrong_user", "wrong_pass")

        # make sure we are NOT logged in
        assert not lp.is_logged_in(timeout=3), "Unexpectedly logged in with invalid credentials"

        # then check for an error message (toast/alert/label)
        error = lp.get_error_message(timeout=6)
        assert error is not None and error.strip() != "", f"Expected an error message but got: {error}"

    def test_logout(self, driver, wait):
        lp = LoginPage(driver, wait)
        lp.login("standard_user", "secret_sauce")
        assert lp.is_logged_in()
        lp.logout()
        # after logout, login button should be visible again
        assert driver.find_element(*lp.login_button_locator), "Login button not visible after logout"
