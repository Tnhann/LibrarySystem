from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class BooksPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    # Locators
    SEARCH_INPUT = (By.NAME, "searchString")
    CATEGORY_SELECT = (By.NAME, "categoryId")
    AVAILABILITY_SELECT = (By.NAME, "availability")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    def search_book(self, search_text):
        search_input = self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUT))
        search_input.clear()
        search_input.send_keys(search_text)
        
    def select_category(self, category_name):
        category_select = Select(self.wait.until(EC.presence_of_element_located(self.CATEGORY_SELECT)))
        category_select.select_by_visible_text(category_name)
        
    def select_availability(self, availability):
        avail_select = Select(self.wait.until(EC.presence_of_element_located(self.AVAILABILITY_SELECT)))
        avail_select.select_by_visible_text(availability) 