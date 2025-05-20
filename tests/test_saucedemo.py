import tempfile

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    profile_dir = tempfile.mkdtemp(prefix="chrome-profile-")
    options.add_argument(f"--user-data-dir={profile_dir}")

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()


def login(driver, username: str, password: str):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


def test_successful_login(driver):
    login(driver, "standard_user", "secret_sauce")
    assert "inventory.html" in driver.current_url


def test_unsuccessful_login(driver):
    login(driver, "standard_user", "wrong_password")
    err = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
    assert "Username and password do not match any user in this service" in err


def test_redirect_after_login(driver):
    login(driver, "standard_user", "secret_sauce")
    assert driver.current_url == "https://www.saucedemo.com/inventory.html"


def test_add_to_cart_button_changes(driver):
    login(driver, "standard_user", "secret_sauce")
    add_btn = driver.find_element(By.ID, "add-to-cart-sauce-labs-onesie")
    assert add_btn.text.lower() == "add to cart"
    add_btn.click()
    remove_btn = driver.find_element(By.ID, "remove-sauce-labs-onesie")
    assert remove_btn.text.lower() == "remove"


def test_product_appears_in_cart(driver):
    login(driver, "standard_user", "secret_sauce")
    driver.find_element(By.ID, "add-to-cart-sauce-labs-onesie").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert any("Sauce Labs Onesie" in item.text for item in items), f"Actual items: {[item.text for item in items]}"
