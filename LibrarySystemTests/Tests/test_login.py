from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_login_page(browser):
    # Test URL'sini güncelleyin
    browser.get("http://127.0.0.1:5000")
    
    try:
        # Sayfanın yüklenmesi için kısa bir bekleme
        time.sleep(2)
        
        # Sayfa kaynağını yazdır (debug için)
        print("Sayfa Kaynağı:")
        print(browser.page_source)
        
        # Login elementlerini farklı seçicilerle bulmayı dene
        username_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
            # Alternatif seçiciler:
            # By.NAME, "username"
            # By.CSS_SELECTOR, "#username"
            # By.XPATH, "//input[@id='username']"
        )
        
        password_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        
        login_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )
        
        # Bilgileri gir
        username_input.send_keys("test_user")
        password_input.send_keys("test_password")
        
        # Login butonuna tıkla
        login_button.click()
        
        # Giriş başarılı mı kontrol et
        success_message = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        
        assert "Başarıyla giriş yapıldı" in success_message.text
        
    except Exception as e:
        print(f"Test sırasında hata oluştu: {str(e)}")
        # Hata durumunda ekran görüntüsü al
        browser.save_screenshot("error_screenshot.png")
        raise 