from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
    # Locators
    USERNAME_INPUT = (By.NAME, "Username")
    PASSWORD_INPUT = (By.NAME, "Password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    def login(self, username, password):
        self.wait.until(EC.element_to_be_clickable(self.USERNAME_INPUT)).send_keys(username)
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD_INPUT)).send_keys(password)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click() 