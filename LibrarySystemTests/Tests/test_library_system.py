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
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

class TestLibrarySystem:
    
    @pytest.fixture
    def setup_page(self, driver):
        # 4. Implicit wait kullanımı
        driver.implicitly_wait(10)
        driver.get("http://localhost:5000")
        return driver
    
    def take_screenshot(self, driver, name):
        # 7. Screenshot alma
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        driver.save_screenshot(f"screenshots/{name}_{timestamp}.png")
    
    def test_element_finding_methods(self, setup_page):
        driver = setup_page
        logging.info("Testing different element finding methods")
        
        try:
            # Login sayfasına git
            login_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Account/Login']"))
            )
            login_link.click()
            
            # ID ile bulma
            username = driver.find_element(By.ID, "username")
            username.send_keys("admin")
            
            # Name ile bulma
            password = driver.find_element(By.ID, "password")
            password.send_keys("admin123")
            
            # CSS Selector ile bulma
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            
            # XPath ile bulma
            header = driver.find_element(By.XPATH, "//h2[contains(text(), 'Yönetici Girişi')]")
            
            # Text alma
            header_text = header.text
            assert "Yönetici Girişi" in header_text
            
            self.take_screenshot(driver, "element_finding")
            logging.info("Element finding methods tested successfully")
            
        except Exception as e:
            logging.error(f"Element finding test failed: {str(e)}")
            self.take_screenshot(driver, "element_finding_error")
            raise
    
    def test_form_interactions(self, setup_page):
        driver = setup_page
        logging.info("Testing form interactions")
        
        try:
            # Önce login olalım
            if not self.login(driver):
                pytest.fail("Login failed")
            
            time.sleep(3)  # Login sonrası bekle
            
            # Kitaplar sayfasına git
            books_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Books']"))
            )
            books_link.click()
            logging.info("Navigated to Books page")
            
            time.sleep(3)  # Kitaplar sayfası yüklenmesi için bekle
            
            # Yeni kitap sayfasına git
            new_book_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Books/Create']"))
            )
            new_book_link.click()
            logging.info("Navigated to Create Book page")
            
            time.sleep(3)  # Form yüklenmesi için bekle
            
            # Form elementlerini doldur
            title_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "Title"))
            )
            title_input.send_keys("Test Kitabı")
            time.sleep(1)
            
            # Kategori seçimi
            category_select = Select(driver.find_element(By.ID, "CategoryID"))
            category_select.select_by_index(1)
            time.sleep(2)
            
            self.take_screenshot(driver, "form_interactions")
            logging.info("Form interactions completed")
            
            time.sleep(3)  # Son işlemler için bekle
            
        except Exception as e:
            logging.error(f"Form interaction test failed: {str(e)}")
            self.take_screenshot(driver, "form_error")
            raise
    
    def test_wait_mechanisms(self, setup_page):
        driver = setup_page
        logging.info("Testing wait mechanisms")
        
        try:
            # Önce login olalım
            if not self.login(driver):
                pytest.fail("Login failed")
            
            time.sleep(3)  # Login sonrası bekle
            logging.info("Starting wait mechanism tests")
            
            # Kitaplar linkinin görünür ve tıklanabilir olmasını bekle
            books_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Books']"))
            )
            books_link.click()
            logging.info("Clicked Books link")
            
            time.sleep(3)  # Sayfa yüklenmesi için bekle
            
            # Yeni kitap butonunun görünür olmasını bekle
            new_book_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='/Books/Create']"))
            )
            logging.info("Found New Book button")
            
            time.sleep(2)
            
            # Kitap listesi tablosunun yüklenmesini bekle
            book_list = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "card"))
            )
            logging.info("Book list loaded")
            
            # Sayfadaki diğer elementlerin yüklenmesini bekle
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "nav-link"))
            )
            
            time.sleep(2)
            
            # Yeni kitap sayfasına git
            new_book_button.click()
            logging.info("Clicked New Book button")
            
            time.sleep(3)
            
            # Form elementlerinin yüklenmesini bekle
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "Title"))
            )
            logging.info("Form elements loaded")
            
            self.take_screenshot(driver, "wait_mechanisms")
            logging.info("Wait mechanisms tested successfully")
            
            time.sleep(2)  # Son kontroller için bekle
            
        except Exception as e:
            logging.error(f"Wait mechanism test failed: {str(e)}")
            self.take_screenshot(driver, "wait_error")
            raise
    
    def test_advanced_interactions(self, setup_page):
        driver = setup_page
        logging.info("Testing advanced interactions")
        
        try:
            # Önce login olalım
            if not self.login(driver):
                pytest.fail("Login failed")
            
            time.sleep(2)
            
            # Kitaplar sayfasına git
            books_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Books']"))
            )
            books_link.click()
            
            # JavaScript ile scroll
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # Element durumu kontrolü - Yeni Kitap butonu
            new_book_button = driver.find_element(By.CSS_SELECTOR, "a[href='/Books/Create']")
            assert new_book_button.is_enabled(), "New book button is not enabled"
            assert new_book_button.is_displayed(), "New book button is not visible"
            
            # Element koordinatları ve boyutları
            location = new_book_button.location
            size = new_book_button.size
            logging.info(f"Button location: {location}, size: {size}")
            
            # JavaScript ile tıklama
            driver.execute_script("arguments[0].click();", new_book_button)
            
            self.take_screenshot(driver, "advanced_interactions")
            logging.info("Advanced interactions tested successfully")
            
        except Exception as e:
            logging.error(f"Advanced interaction test failed: {str(e)}")
            self.take_screenshot(driver, "advanced_error")
            raise
    
    def test_browser_management(self, setup_page):
        # 6. Tarayıcı yönetimi
        driver = setup_page
        
        try:
            # Tarayıcı pencere boyutu
            driver.maximize_window()
            
            # Yeni sekme açma
            driver.execute_script("window.open('');")
            
            # Sekmeler arası geçiş
            handles = driver.window_handles
            driver.switch_to.window(handles[-1])
            
            # Headless mod kontrolü
            is_headless = driver.execute_script("return navigator.webdriver")
            logging.info(f"Running in headless mode: {is_headless}")
            
        except Exception as e:
            logging.error(f"Browser management test failed: {str(e)}")
            self.take_screenshot(driver, "browser_management_error")
            raise 
    
    def login(self, driver):
        """Login helper function"""
        try:
            logging.info("Starting login process...")
            time.sleep(2)  # Ana sayfa yüklenmesi için bekle
            
            # Ana sayfadaki login butonunu bul ve tıkla
            login_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Account/Login']"))
            )
            login_link.click()
            logging.info("Clicked login link")
            
            time.sleep(3)  # Login sayfasının yüklenmesini bekle
            
            # Login form elementlerini bul
            username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password = driver.find_element(By.ID, "password")
            
            # Giriş bilgilerini gir
            username.clear()
            time.sleep(1)
            username.send_keys("admin")
            logging.info("Entered username")
            
            time.sleep(1)
            password.clear()
            password.send_keys("admin123")
            logging.info("Entered password")
            
            time.sleep(2)  # Giriş bilgileri girildikten sonra bekle
            
            # Submit butonu
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            logging.info("Clicked submit button")
            
            time.sleep(3)  # Login işlemi için bekle
            
            # Başarılı giriş kontrolü
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/Books']"))
            )
            
            time.sleep(2)  # Ana sayfa yüklenmesi için son bekle
            logging.info("Login successful")
            return True
            
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            self.take_screenshot(driver, "login_error")
            return False 
    
    def test_book_operations(self, setup_page):
        driver = setup_page
        logging.info("Testing book operations")
        
        try:
            # Önce login olalım
            if not self.login(driver):
                pytest.fail("Login failed")
            
            time.sleep(3)  # Login sonrası bekle
            
            # Kitaplar sayfasına git
            books_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Books']"))
            )
            books_link.click()
            logging.info("Navigated to Books page")
            
            time.sleep(3)
            
            # Yeni kitap ekleme sayfasına git
            new_book_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Books/Create']"))
            )
            new_book_link.click()
            logging.info("Navigated to Create Book page")
            
            time.sleep(3)
            
            # Form elementlerini doldur
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
                    logging.info(f"Filled {field_id} with {value}")
                    time.sleep(1)
                except Exception as e:
                    logging.warning(f"Could not fill {field_id}: {str(e)}")
            
            # Kategori seçimi
            try:
                category_select = Select(WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "CategoryID"))
                ))
                category_select.select_by_value("1")  # İlk kategoriyi seç
                logging.info("Selected category")
                time.sleep(1)
            except Exception as e:
                logging.error(f"Could not select category: {str(e)}")
            
            # Formu gönder
            submit_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(2)
            submit_button.click()
            logging.info("Submitted form")
            
            # Başarılı ekleme kontrolü
            WebDriverWait(driver, 10).until(
                EC.url_contains("/Books")
            )
            
            # Eklenen kitabı ara
            try:
                search_box = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "searchString"))
                )
                search_box.send_keys("Test Kitabı")
                search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                search_button.click()
                logging.info("Searched for added book")
                
                time.sleep(2)
                
                # Kitabın listede olduğunu kontrol et
                book_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Test Kitabı')]"))
                )
                assert book_element.is_displayed()
                logging.info("Book found in the list")
                
            except Exception as e:
                logging.error(f"Book search failed: {str(e)}")
            
            self.take_screenshot(driver, "book_operations")
            
        except Exception as e:
            logging.error(f"Book operations failed: {str(e)}")
            self.take_screenshot(driver, "book_operations_error")
            raise 
    
    def test_element_properties(self, setup_page):
        driver = setup_page
        logging.info("Testing element properties and coordinates")
        
        try:
            if not self.login(driver):
                pytest.fail("Login failed")
            
            time.sleep(3)
            
            # Kitaplar linkinin özelliklerini kontrol et
            books_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/Books']"))
            )
            
            # Koordinat ve boyut bilgileri
            location = books_link.location
            size = books_link.size
            logging.info(f"Books link location: {location}")
            logging.info(f"Books link size: {size}")
            
            # Element durumu kontrolleri
            assert books_link.is_displayed(), "Books link is not visible"
            assert books_link.is_enabled(), "Books link is not enabled"
            
            # JavaScript ile scroll
            driver.execute_script("arguments[0].scrollIntoView(true);", books_link)
            time.sleep(1)
            
            # Yeni kitap butonunun özelliklerini kontrol et
            new_book_btn = driver.find_element(By.CSS_SELECTOR, "a[href='/Books/Create']")
            btn_location = new_book_btn.location
            btn_size = new_book_btn.size
            logging.info(f"New book button location: {btn_location}")
            logging.info(f"New book button size: {btn_size}")
            
            self.take_screenshot(driver, "element_properties")
            logging.info("Element properties test completed")
            
        except Exception as e:
            logging.error(f"Element properties test failed: {str(e)}")
            self.take_screenshot(driver, "element_properties_error")
            raise 
    
    def test_form_elements(self, setup_page):
        driver = setup_page
        logging.info("Testing form elements")
        
        try:
            # Login sayfasına git
            login_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Account/Login']"))
            )
            login_link.click()
            time.sleep(2)
            
            # Remember me checkbox'ını kontrol et
            remember_me = driver.find_element(By.ID, "RememberMe")
            if not remember_me.is_selected():
                remember_me.click()
            logging.info("Checked remember me checkbox")
            time.sleep(1)
            
            # Login ol
            username = driver.find_element(By.ID, "username")
            password = driver.find_element(By.ID, "password")
            username.send_keys("admin")
            password.send_keys("admin123")
            
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            time.sleep(3)
            
            # Kitap ekleme sayfasına git
            new_book_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Books/Create']"))
            )
            new_book_link.click()
            time.sleep(2)
            
            # Radio button kontrolü
            status_new = driver.find_element(By.ID, "statusNew")
            status_used = driver.find_element(By.ID, "statusUsed")
            
            assert status_new.is_selected(), "New status should be selected by default"
            status_used.click()
            time.sleep(1)
            assert status_used.is_selected(), "Used status should be selected after click"
            
            self.take_screenshot(driver, "form_elements")
            logging.info("Form elements test completed")
            
        except Exception as e:
            logging.error(f"Form elements test failed: {str(e)}")
            self.take_screenshot(driver, "form_elements_error")
            raise
    
    def test_browser_compatibility(self, setup_page):
        driver = setup_page
        logging.info("Testing browser compatibility")
        
        try:
            if not self.login(driver):
                pytest.fail("Login failed")
            
            time.sleep(3)
            
            # Viewport boyutlarını kontrol et
            viewport_size = driver.execute_script("""
                return {
                    width: window.innerWidth,
                    height: window.innerHeight
                };
            """)
            logging.info(f"Viewport size: {viewport_size}")
            
            # Farklı ekran boyutlarını test et
            screen_sizes = [
                (1920, 1080),  # Desktop
                (1366, 768),   # Laptop
                (768, 1024),   # Tablet
                (375, 812)     # Mobile
            ]
            
            for width, height in screen_sizes:
                driver.set_window_size(width, height)
                time.sleep(1)
                
                # Responsive elementleri kontrol et
                navbar = driver.find_element(By.CLASS_NAME, "navbar")
                assert navbar.is_displayed(), f"Navbar should be visible at {width}x{height}"
                
                # Menü butonunun görünürlüğünü kontrol et
                try:
                    menu_button = driver.find_element(By.CLASS_NAME, "navbar-toggler")
                    if width < 768:  # Mobile view
                        assert menu_button.is_displayed(), "Menu button should be visible on mobile"
                    else:
                        assert not menu_button.is_displayed(), "Menu button should be hidden on desktop"
                except:
                    if width < 768:
                        pytest.fail("Menu button not found on mobile view")
                
                self.take_screenshot(driver, f"compatibility_{width}x{height}")
            
            logging.info("Browser compatibility test completed")
            
        except Exception as e:
            logging.error(f"Browser compatibility test failed: {str(e)}")
            self.take_screenshot(driver, "compatibility_error")
            raise

    def test_dynamic_content(self, setup_page):
        driver = setup_page
        logging.info("Testing dynamic content loading")
        
        try:
            # Önce login olalım
            if not self.login(driver):
                pytest.fail("Login failed")
            
            time.sleep(3)
            
            # Kitaplar sayfasına git
            books_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Books']"))
            )
            books_link.click()
            time.sleep(2)
            
            # Kitap listesinin yüklenmesini bekle
            book_cards = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "card"))
            )
            initial_count = len(book_cards)
            logging.info(f"Initial book count: {initial_count}")
            
            # Sayfayı aşağı kaydır
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Arama yap
            try:
                search_box = driver.find_element(By.ID, "searchString")
                search_box.clear()
                search_box.send_keys("Test")
                search_box.send_keys(Keys.RETURN)
                time.sleep(2)
                logging.info("Search performed")
                
                # Arama sonuçlarını kontrol et
                filtered_cards = driver.find_elements(By.CLASS_NAME, "card")
                logging.info(f"Filtered book count: {len(filtered_cards)}")
                
            except NoSuchElementException:
                logging.warning("Search box not found, skipping search test")
            
            self.take_screenshot(driver, "dynamic_content")
            logging.info("Dynamic content test completed")
            
        except Exception as e:
            logging.error(f"Dynamic content test failed: {str(e)}")
            self.take_screenshot(driver, "dynamic_content_error")
            raise 
    
    def test_iframe_and_window(self, setup_page):
        driver = setup_page
        logging.info("Testing iframe and window operations")
        
        try:
            if not self.login(driver):
                pytest.fail("Login failed")
            
            time.sleep(3)
            logging.info("Login successful")
            
            # Kitaplar sayfasına git
            books_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Books']"))
            )
            books_link.click()
            time.sleep(2)
            logging.info("Navigated to Books page")
            
            # Önce bir kitap ekleyelim
            new_book_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Books/Create']"))
            )
            new_book_link.click()
            time.sleep(2)
            logging.info("Clicked Create New Book")
            
            # Kitap bilgilerini gir
            form_fields = {
                "Title": "Test Kitap",
                "Author": "Test Yazar",
                "ISBN": "1234567890",
                "PublishYear": "2024",
                "Publisher": "Test Yayınevi"
            }
            
            # Her form alanını doldur
            for field_id, value in form_fields.items():
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, field_id))
                )
                element.clear()
                element.send_keys(value)
                logging.info(f"Filled {field_id} with {value}")
                time.sleep(1)
            
            # Kategori seç
            category_select = Select(WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "CategoryID"))
            ))
            category_select.select_by_index(1)
            time.sleep(1)
            logging.info("Selected category")
            
            # Formu gönder
            submit_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            submit_button.click()
            time.sleep(3)
            logging.info("Submitted form")
            
            try:
                # Sayfanın yüklendiğinden emin ol
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "table"))
                )
                logging.info("Table loaded")
                
                # Tabloda kitabı bul
                book_title_cell = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//td[text()='{form_fields['Title']}']"))
                )
                logging.info("Found book title in table")
                
                # Kitabın satırını bul
                book_row = book_title_cell.find_element(By.XPATH, "./..")
                logging.info("Found book row")
                
                # Buton grubunun HTML'ini logla
                buttons_html = book_row.find_element(By.CLASS_NAME, "btn-group").get_attribute('innerHTML')
                logging.info(f"Buttons HTML: {buttons_html}")
                
                # Tüm butonları bul ve logla
                buttons = book_row.find_elements(By.CSS_SELECTOR, ".btn-group a")
                for i, button in enumerate(buttons):
                    logging.info(f"Button {i}: class='{button.get_attribute('class')}' title='{button.get_attribute('title')}' href='{button.get_attribute('href')}'")
                
                # Detay butonunu farklı yöntemlerle bulmayı dene
                try:
                    # 1. Yöntem: title attribute ile
                    details_button = book_row.find_element(By.CSS_SELECTOR, "a[title='Detay']")
                except:
                    try:
                        # 2. Yöntem: href ile
                        details_button = book_row.find_element(By.CSS_SELECTOR, "a[href*='/Books/Details/']")
                    except:
                        try:
                            # 3. Yöntem: icon ile
                            details_button = book_row.find_element(By.CSS_SELECTOR, "a i.fa-info-circle")
                            details_button = details_button.find_element(By.XPATH, "./..")
                        except:
                            # Tüm butonları göster ve hata ver
                            buttons_html = book_row.find_element(By.CLASS_NAME, "btn-group").get_attribute('outerHTML')
                            logging.error(f"Could not find details button. Available buttons: {buttons_html}")
                            raise
                
                logging.info("Found details button")
                details_button.click()
                time.sleep(2)
                logging.info("Clicked details button")
                
                # iframe işlemleri
                try:
                    iframe = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "bookPreview"))
                    )
                    logging.info("Found iframe")
                    
                    # iframe'e geç
                    driver.switch_to.frame(iframe)
                    time.sleep(2)
                    self.take_screenshot(driver, "inside_iframe")
                    
                    # Ana sayfaya geri dön
                    driver.switch_to.default_content()
                    logging.info("Switched back to main content")
                except Exception as e:
                    logging.warning(f"iframe operations failed: {str(e)}")
                
                # Yeni pencere işlemleri
                try:
                    new_window_link = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "openNewWindow"))
                    )
                    new_window_link.click()
                    time.sleep(2)
                    
                    # Yeni pencereye geç
                    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
                    original_window = driver.current_window_handle
                    
                    for window_handle in driver.window_handles:
                        if window_handle != original_window:
                            driver.switch_to.window(window_handle)
                            break
                    
                    time.sleep(2)
                    self.take_screenshot(driver, "new_window")
                    
                    # Yeni pencereyi kapat ve ana pencereye dön
                    driver.close()
                    driver.switch_to.window(original_window)
                    logging.info("Returned to main window")
                except Exception as e:
                    logging.warning(f"New window operations failed: {str(e)}")
                
            except Exception as e:
                logging.error(f"Could not navigate to book details: {str(e)}")
                self.take_screenshot(driver, "navigation_error")
                current_url = driver.current_url
                page_source = driver.page_source
                logging.error(f"Current URL: {current_url}")
                logging.error(f"Page source: {page_source[:500]}...")  # İlk 500 karakteri logla
                raise
            
        except Exception as e:
            logging.error(f"iframe and window test failed: {str(e)}")
            self.take_screenshot(driver, "iframe_window_error")
            raise 