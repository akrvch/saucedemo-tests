import tempfile

import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "disable-save-password-bubble"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=PasswordLeakDetection,SavePasswordBubble")
    options.add_argument("--disable-features=TranslateUI,AutofillServerCommunication,PasswordManager")
    profile_dir = tempfile.mkdtemp(prefix="chrome-profile-")
    options.add_argument(f"--user-data-dir={profile_dir}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def login(driver, username: str, password: str):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(
        EC.any_of(
            EC.url_contains("inventory.html"),
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
        )
    )


def test_successful_login(driver):
    login(driver, "standard_user", "secret_sauce")
    assert "inventory.html" in driver.current_url


def test_unsuccessful_login(driver):
    login(driver, "standard_user", "wrong_password")
    err = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    ).text
    assert "Username and password do not match any user in this service" in err


def test_redirect_after_login(driver):
    login(driver, "standard_user", "secret_sauce")
    assert driver.current_url.endswith("inventory.html")


def test_add_to_cart_button_changes(driver):
    login(driver, "standard_user", "secret_sauce")
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-onesie"))
    )
    assert btn.text.lower() == "add to cart"
    btn.click()
    remove_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "remove-sauce-labs-onesie"))
    )
    assert remove_btn.text.lower() == "remove"


def test_product_appears_in_cart(driver):
    login(driver, "standard_user", "secret_sauce")
    try:
        add_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-onesie"))
        )
        add_btn.click()
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"), "1")
        )
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "cart_item"))
        )
        assert any("Sauce Labs Onesie" in item.text for item in items)
    except TimeoutException:
        print("Timeout occurred. Page source:", driver.page_source)
        raise