from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_page(browser):
    # Siteye git
    browser.get("http://localhost:5000")  # veya kendi URL'niz
    
    # Login elementlerini bul
    username_input = browser.find_element(By.ID, "username")
    password_input = browser.find_element(By.ID, "password")
    login_button = browser.find_element(By.ID, "login-button")
    
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