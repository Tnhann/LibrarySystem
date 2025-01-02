import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_objects.login_page import LoginPage
from page_objects.books_page import BooksPage
import logging
import os
from datetime import datetime

def take_screenshot(driver, name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    driver.save_screenshot(f"{screenshot_dir}/{name}_{timestamp}.png")

@pytest.mark.parallel
class TestLibrarySystem:
    
    def test_login(self, browser):
        login_page = LoginPage(browser)
        browser.get("http://localhost:5000/Account/Login")
        
        try:
            login_page.login("admin", "admin123")
            assert "Ana Sayfa" in browser.title
            logging.info("Login successful")
            take_screenshot(browser, "login_success")
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            take_screenshot(browser, "login_error")
            raise
    
    def test_book_search(self, browser):
        self.test_login(browser)
        books_page = BooksPage(browser)
        browser.get("http://localhost:5000/Books")
        
        try:
            # İframe varsa geç
            if len(browser.find_elements_by_tag_name("iframe")) > 0:
                browser.switch_to.frame(0)
            
            books_page.search_book("1984")
            books_page.select_category("Roman")
            books_page.select_availability("Mevcut")
            
            # JavaScript ile scroll
            element = browser.find_element_by_css_selector("table")
            browser.execute_script("arguments[0].scrollIntoView(true);", element)
            
            # Element boyutlarını al
            size = element.size
            location = element.location
            logging.info(f"Table size: {size}, location: {location}")
            
            take_screenshot(browser, "search_results")
            assert "1984" in browser.page_source
            
        except Exception as e:
            logging.error(f"Book search failed: {str(e)}")
            take_screenshot(browser, "search_error")
            raise
        finally:
            if len(browser.find_elements_by_tag_name("iframe")) > 0:
                browser.switch_to.default_content()

if __name__ == "__main__":
    pytest.main(["-v", "-n=3", "--html=report.html"]) 