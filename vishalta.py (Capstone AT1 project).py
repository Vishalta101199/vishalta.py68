orange_hrm/
│
├── config/
│   └── config.ini
│
├── data/
│   └── test_data.csv
│
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── pim_page.py
│
└── tests/
    ├── test_login.py
    └── test_pim.py

mkdir orange_hrm
cd orange_hrm
mkdir config data pages tests
pip install selenium pytest configparser pandas

[DEFAULT]
url = http://orangehrm3.com
username = Admin
password = admin123
invalid_password = wrongpass

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))

from selenium.webdriver.common.by import By
from pages.base_page.py import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "txtUsername")
    PASSWORD_INPUT = (By.ID, "txtPassword")
    LOGIN_BUTTON = (By.ID, "btnLogin")
    ERROR_MESSAGE = (By.ID, "spanMessage")

    def enter_username(self, username):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text

from selenium.webdriver.common.by import By
from pages.base_page.py import BasePage

class PimPage(BasePage):
    ADD_BUTTON = (By.ID, "btnAdd")
    SAVE_BUTTON = (By.ID, "btnSave")
    FIRST_NAME_INPUT = (By.ID, "firstName")
    LAST_NAME_INPUT = (By.ID, "lastName")
    EMPLOYEE_ID_INPUT = (By.ID, "employeeId")

    def click_add(self):
        self.driver.find_element(*self.ADD_BUTTON).click()

    def enter_employee_details(self, first_name, last_name, emp_id):
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(*self.EMPLOYEE_ID_INPUT).send_keys(emp_id)

    def click_save(self):
        self.driver.find_element(*self.SAVE_BUTTON).click()

username,password,expected_result
Admin,admin123,success
Admin,wrongpass,Invalid credentials

import pytest
import csv
from selenium import webdriver
from pages.login_page import LoginPage
from configparser import ConfigParser

@pytest.fixture
def config():
    parser = ConfigParser()
    parser.read('config/config.ini')
    return parser['DEFAULT']

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get(config['url'])
    yield driver
    driver.quit()

@pytest.mark.parametrize("username,password,expected_result", [
    ("Admin", "admin123", "success"),
    ("Admin", "wrongpass", "Invalid credentials")
])
def test_login(username, password, expected_result, driver):
    login_page = LoginPage(driver)
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()
    if expected_result == "success":
        assert driver.current_url == "expected_dashboard_url"
    else:
        assert login_page.get_error_message() == expected_result

import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.pim_page import PimPage
from configparser import ConfigParser

@pytest.fixture
def config():
    parser = ConfigParser()
    parser.read('config/config.ini')
    return parser['DEFAULT']

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get(config['url'])
    login_page = LoginPage(driver)
    login_page.enter_username(config['username'])
    login_page.enter_password(config['password'])
    login_page.click_login()
    yield driver
    driver.quit()

def test_add_employee(driver):
    pim_page = PimPage(driver)
    pim_page.click_add()
    pim_page.enter_employee_details("John", "Doe", "1234")
    pim_page.click_save()
    assert driver.find_element(By.ID, "success_message_id").is_displayed()

def test_edit_employee(driver):
    pim_page = PimPage(driver)
    pim_page.edit_employee("John", "Doe", "1234")
    pim_page.click_save()
    assert driver.find_element(By.ID, "success_message_id").is_displayed()

def test_delete_employee(driver):
    pim_page = PimPage(driver)
    pim_page.delete_employee("1234")
    assert driver.find_element(By.ID, "success_message_id").is_displayed()


