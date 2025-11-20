# file: test_browser.py
from selenium import webdriver


def test_login_page():
    driver = webdriver.Edge()  # 或 Firefox()
    driver.get("http://127.0.0.1:5000/login")
    assert "登录" in driver.page_source
    driver.quit()