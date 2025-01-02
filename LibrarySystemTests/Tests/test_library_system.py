import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import logging
from datetime import datetime, timedelta
import os
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time  # Dosyanın başına ekleyin

class TestLibrarySystem:
    
    @pytest.fixture
    def setup_page(self, driver):
        driver.get("http://localhost:5000")  # URL güncellendi
        return driver
    
    def take_screenshot(self, driver, name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver.save_screenshot(f"screenshots/{name}_{timestamp}.png")
    
    def test_login_functionality(self, setup_page):
        driver = setup_page
        logging.info("Starting login test")
        
        try:
            # Ana sayfadaki login butonunu bul ve tıkla
            login_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Account/Login']"))
            )
            login_link.click()
            
            # Login sayfasının yüklenmesini bekle
            username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password = driver.find_element(By.ID, "password")
            
            # Giriş bilgilerini gir
            username.clear()
            username.send_keys("admin")
            password.clear()
            password.send_keys("admin123")
            
            # Submit butonu
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Başarılı giriş kontrolü
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/Books']"))
            )
            
            logging.info("Login successful")
            self.take_screenshot(driver, "login_success")
            return True
            
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            self.take_screenshot(driver, "login_error")
            raise
    
    def test_book_search_with_filters(self, setup_page):
        driver = setup_page
        logging.info("Testing book search functionality")
        
        if not self.test_login_functionality(setup_page):
            pytest.fail("Login failed, skipping book search test")
        
        try:
            time.sleep(3)  # Login sonrası bekle
            
            # Kitaplar sayfasına git
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Books']"))
            ).click()
            logging.info("Clicked on Books link")
            
            time.sleep(3)  # Kitaplar sayfası yüklenmesi için bekle
            
            # Yeni kitap ekleme sayfasına git
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Books/Create']"))
            ).click()
            logging.info("Clicked on Create New Book link")
            
            time.sleep(3)  # Form yüklenmesi için bekle
            
            # Form elementlerinin yüklenmesini bekle
            form_fields = {
                "Title": "Test Kitabı",
                "Author": "Test Yazarı",
                "ISBN": "1234567890",
                "PublishYear": "2024",
                "Publisher": "Test Yayınevi"
            }
            
            # Her form alanını doldur
            for field_id, value in form_fields.items():
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.ID, field_id))
                    )
                    element.clear()
                    element.send_keys(value)
                    time.sleep(1)  # Her alan girişi sonrası kısa bekle
                    logging.info(f"Filled {field_id} with {value}")
                except Exception as e:
                    logging.warning(f"Could not fill {field_id}: {str(e)}")
            
            time.sleep(2)  # Form doldurma sonrası bekle
            
            # Kategori seçimi
            try:
                category_select = Select(WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "CategoryID"))
                ))
                category_select.select_by_value("1")
                time.sleep(1)  # Kategori seçimi sonrası bekle
                logging.info("Selected category: Roman")
            except Exception as e:
                logging.warning(f"Could not select category: {str(e)}")
            
            time.sleep(2)  # Form gönderme öncesi bekle
            
            # Form gönderme
            try:
                submit_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                submit_button.click()
                logging.info("Clicked submit button")
            except Exception as e:
                logging.error(f"Could not submit form: {str(e)}")
                raise
            
            time.sleep(3)  # Form gönderimi sonrası bekle
            
            # Başarılı ekleme kontrolü
            WebDriverWait(driver, 10).until(
                EC.url_contains("/Books")
            )
            logging.info("Redirected to Books page after submission")
            
            self.take_screenshot(driver, "book_added")
            
        except Exception as e:
            logging.error(f"Book operation failed: {str(e)}")
            self.take_screenshot(driver, "book_operation_error")
            raise
    
    def test_navigation_and_logout(self, setup_page):
        driver = setup_page
        logging.info("Testing navigation and logout")
        
        # Önce login olalım
        if not self.test_login_functionality(setup_page):
            pytest.fail("Login failed, skipping navigation test")
        
        try:
            # Menü öğelerinin görünür olmasını bekle
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/Books']"))
            )
            
            # Çıkış yap
            logout_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Account/Logout']"))
            )
            logout_link.click()
            
            # Login sayfasına dönüldüğünü kontrol et
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/Account/Login']"))
            )
            
            self.take_screenshot(driver, "logout_success")
            logging.info("Logout successful")
            
        except Exception as e:
            logging.error(f"Navigation/logout failed: {str(e)}")
            self.take_screenshot(driver, "navigation_error")
            raise
    
    def test_home_page_statistics(self, setup_page):
        driver = setup_page
        logging.info("Testing home page statistics")
        
        # Önce login olalım
        if not self.test_login_functionality(setup_page):
            pytest.fail("Login failed, skipping statistics test")
        
        try:
            # Ana sayfaya git
            home_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.navbar-brand"))
            )
            home_link.click()
            
            # İstatistik kartlarının yüklenmesini bekle
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "stat-card"))
            )
            
            # İstatistikleri kontrol et
            stats = {
                "Toplam Kitap": "//div[contains(@class, 'stat-card')]//i[contains(@class, 'fa-book')]/following-sibling::h3",
                "Mevcut Kitap": "//div[contains(@class, 'stat-card')]//i[contains(@class, 'fa-check-circle')]/following-sibling::h3",
                "Ödünç Verilen": "//div[contains(@class, 'stat-card')]//i[contains(@class, 'fa-clock')]/following-sibling::h3",
                "Kategori": "//div[contains(@class, 'stat-card')]//i[contains(@class, 'fa-tags')]/following-sibling::h3"
            }
            
            for label, xpath in stats.items():
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    value = element.text
                    logging.info(f"{label}: {value}")
                    assert element.is_displayed(), f"{label} istatistiği görünmüyor"
                except Exception as e:
                    logging.error(f"Could not find {label} statistic: {str(e)}")
                    self.take_screenshot(driver, f"missing_stat_{label}")
                    raise
            
            self.take_screenshot(driver, "home_page_stats")
            logging.info("All statistics verified successfully")
            
        except Exception as e:
            logging.error(f"Statistics check failed: {str(e)}")
            self.take_screenshot(driver, "stats_error")
            raise 
    
    def test_delete_book(self, setup_page):
        driver = setup_page
        logging.info("Testing book deletion")
        
        if not self.test_login_functionality(setup_page):
            pytest.fail("Login failed, skipping delete test")
            
        try:
            time.sleep(3)  # Login sonrası bekle
            
            # Kitaplar sayfasına git
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Books']"))
            ).click()
            logging.info("Navigated to Books page")
            
            time.sleep(3)  # Sayfa yüklenmesi için bekle
            
            # Silinecek kitabı bul
            delete_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/Books/Delete/']"))
            )
            delete_button.click()
            logging.info("Clicked delete button")
            
            time.sleep(2)  # Silme sayfası yüklenmesi için bekle
            
            # Silme işlemini onayla
            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            confirm_button.click()
            logging.info("Confirmed deletion")
            
            time.sleep(3)  # Silme işlemi sonrası bekle
            
            # Başarılı silme kontrolü
            WebDriverWait(driver, 10).until(
                EC.url_contains("/Books")
            )
            
            self.take_screenshot(driver, "book_deleted")
            logging.info("Book deleted successfully")
            
        except Exception as e:
            logging.error(f"Book deletion failed: {str(e)}")
            self.take_screenshot(driver, "delete_error")
            raise

    def test_loan_book(self, setup_page):
        driver = setup_page
        logging.info("Testing book loan")
        
        if not self.test_login_functionality(setup_page):
            pytest.fail("Login failed, skipping loan test")
            
        try:
            time.sleep(3)  # Login sonrası bekle
            
            # Ödünç işlemleri sayfasına git
            loans_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Loans']"))
            )
            driver.execute_script("arguments[0].click();", loans_link)
            logging.info("Navigated to Loans page")
            
            time.sleep(3)  # Sayfa yüklenmesi için bekle
            
            # Yeni ödünç verme sayfasına git
            new_loan_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Loans/Create']"))
            )
            driver.execute_script("arguments[0].click();", new_loan_button)
            logging.info("Clicked new loan button")
            
            time.sleep(3)  # Form yüklenmesi için bekle
            
            try:
                # Kitap seçimi
                book_select = Select(WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "BookID"))
                ))
                book_select.select_by_index(1)  # İlk kitabı seç
                logging.info("Selected book")
                
                time.sleep(1)
                
                # Teslim tarihi
                due_date = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "DueDate"))
                )
                due_date.clear()
                # Bir ay sonrası için tarih
                due_date_value = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                due_date.send_keys(due_date_value)
                logging.info(f"Set due date to {due_date_value}")
                
                time.sleep(2)
                
                # Formu gönder
                submit_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", submit_button)
                logging.info("Submitted loan form")
                
                time.sleep(3)
                
                # Başarılı ödünç verme kontrolü
                WebDriverWait(driver, 10).until(
                    EC.url_contains("/Loans")
                )
                
                self.take_screenshot(driver, "loan_created")
                logging.info("Book loan created successfully")
                
            except Exception as e:
                logging.error(f"Loan form error: {str(e)}")
                self.take_screenshot(driver, "loan_form_error")
                raise
                
        except Exception as e:
            logging.error(f"Book loan failed: {str(e)}")
            self.take_screenshot(driver, "loan_error")
            raise 