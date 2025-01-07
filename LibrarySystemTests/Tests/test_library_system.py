import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import logging
import os
from datetime import datetime
import time

def setup_logging():
    """8. Logging yapılandırması"""
    log_dir = "test_logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_dir}/test_run_{timestamp}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def take_screenshot(driver, name):
    """7. Screenshot alma"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = "test_screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    filename = f"{screenshot_dir}/{name}_{timestamp}.png"
    driver.save_screenshot(filename)

class TestLibrarySystem:
    """9. pytest kullanımı"""
    BASE_URL = "http://localhost:5000"

    @pytest.fixture(params=["chrome", "firefox", "edge"])
    def driver(self, request):
        """6. Çoklu tarayıcı desteği"""
        browser = request.param
        if browser == "chrome":
            options = ChromeOptions()
            driver = webdriver.Chrome(options=options)
        elif browser == "firefox":
            options = FirefoxOptions()
            driver = webdriver.Firefox(options=options)
        else:
            options = EdgeOptions()
            driver = webdriver.Edge(options=options)
        
        driver.maximize_window()
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def test_all_features(self, driver):
        """Tüm özellikleri test eden ana test fonksiyonu"""
        try:
            setup_logging()
            wait = WebDriverWait(driver, 10)

            # Test adımlarını logla
            logging.info("Test başlıyor...")
            
            # Login işlemi
            logging.info("Login sayfasına gidiliyor...")
            driver.get(f"{self.BASE_URL}/Account/Login")
            
            # 1. Web elementlerini bulma ve metin girme
            logging.info("Kullanıcı adı giriliyor...")
            username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username.send_keys("admin")
            
            logging.info("Şifre giriliyor...")
            password = driver.find_element(By.NAME, "password")
            password.send_keys("admin123")
            
            # 2. Checkbox işlemi
            logging.info("Beni hatırla seçeneği işaretleniyor...")
            remember_me = wait.until(EC.presence_of_element_located((By.NAME, "RememberMe")))
            if not remember_me.is_selected():
                remember_me.click()

            logging.info("Giriş yapılıyor...")
            login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
            login_button.click()

            # Her adımdan sonra kısa bir bekleme ekleyelim ki işlemleri görebilelim
            time.sleep(1)

            logging.info("Ana sayfaya yönlendirme bekleniyor...")
            wait.until(EC.url_to_be(f"{self.BASE_URL}/"))

            logging.info("Kitaplar sayfasına gidiliyor...")
            driver.get(f"{self.BASE_URL}/Books")
            time.sleep(1)

            # 3. Dropdown menü kullanımı
            category_select = Select(wait.until(EC.presence_of_element_located((By.NAME, "categoryId"))))
            category_select.select_by_value("1")  # Roman kategorisi

            # 5. İleri seviye işlemler
            # Yeni kitap ekleme sayfasını yeni pencerede aç
            original_window = driver.current_window_handle
            driver.execute_script("window.open('/Books/Create');")
            
            # Yeni pencereye geçiş
            wait.until(lambda d: len(d.window_handles) > 1)
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break

            # Kitap ekleme formunu doldur
            logging.info("Yeni kitap bilgileri dolduruluyor...")
            
            # Zorunlu alanlar
            title_input = wait.until(EC.presence_of_element_located((By.ID, "Title")))
            title_input.send_keys("Test Kitap")
            
            author_input = driver.find_element(By.ID, "Author")
            author_input.send_keys("Test Yazarı")
            
            # Kategori seçimi (zorunlu)
            book_category = Select(driver.find_element(By.ID, "CategoryID"))
            book_category.select_by_value("1")  # Roman kategorisi
            
            # Opsiyonel alanlar
            isbn_input = driver.find_element(By.ID, "ISBN")
            isbn_input.send_keys("9789750726477")
            
            publish_year = driver.find_element(By.ID, "PublishYear")
            publish_year.send_keys("2024")
            
            publisher_input = driver.find_element(By.ID, "Publisher")
            publisher_input.send_keys("Test Yayınevi")
            
            # Kitap durumu radio button seçimi
            status_new = driver.find_element(By.ID, "statusNew")
            status_used = driver.find_element(By.ID, "statusUsed")
            
            # Yeni kitap olarak işaretle
            if not status_new.is_selected():
                status_new.click()
            
            time.sleep(1)  # Formu görebilmek için kısa bekleme
            
            # Kaydet butonuna tıkla
            submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
            submit_button.click()
            
            # Ana pencereye geri dön
            driver.switch_to.window(original_window)
            
            # Sayfanın yüklenmesini bekle
            time.sleep(2)  # Yönlendirme için kısa bekleme
            
            # Kitaplar sayfasında olduğumuzu kontrol et
            wait.until(EC.url_contains("/Books"))
            
            # Eklenen kitabı listede ara
            search_input = wait.until(EC.presence_of_element_located((By.NAME, "searchString")))
            search_input.clear()
            search_input.send_keys("Test Kitap")
            
            # Arama butonunu bul ve tıkla
            search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            search_button.click()
            
            # Kitabın listelendiğini kontrol et (daha güvenilir bir yöntemle)
            wait.until(EC.presence_of_element_located((
                By.XPATH, 
                "//td[contains(text(), 'Test Kitap')]"
            )))
            logging.info("Eklenen kitap listede görüntülendi")

            # Screenshot al
            take_screenshot(driver, "test_complete")

            # JavaScript ile scroll
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Element durumu kontrolü
            submit_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
            assert submit_button.is_enabled()
            location = submit_button.location
            size = submit_button.size
            logging.info(f"Submit button location: {location}, size: {size}")

            # Metin alma özelliği
            navbar_brand = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "navbar-brand")))
            assert "Kütüphane Sistemi" in navbar_brand.text
            logging.info(f"Sayfa başlığı: {navbar_brand.text}")

            # Dinamik içerik bekleme
            wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

            # iframe işlemi (varsa)
            try:
                help_iframe = wait.until(EC.presence_of_element_located((By.ID, "help-frame")))
                driver.switch_to.frame(help_iframe)
                # iframe içindeki işlemler
                driver.switch_to.default_content()
            except:
                logging.info("Help iframe bulunamadı, devam ediliyor...")

            # Radio button işlemi (varsa)
            try:
                radio_button = wait.until(EC.presence_of_element_located((By.NAME, "bookType")))
                if not radio_button.is_selected():
                    radio_button.click()
            except:
                logging.info("Radio button bulunamadı, devam ediliyor...")

            logging.info("Test başarıyla tamamlandı!")

        except Exception as e:
            logging.error(f"Test sırasında hata: {str(e)}")
            take_screenshot(driver, "test_error")
            raise

if __name__ == "__main__":
    """10. Paralel test çalıştırma"""
    pytest.main(["-v", "-n", "auto", "--dist=loadfile"]) 