# tests/test_smoke.py
def test_smoke(driver):
    assert driver is not None
    try:
        _ = driver.session_id
    except Exception:
        pass
