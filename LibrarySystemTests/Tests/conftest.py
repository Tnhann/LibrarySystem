import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import logging
import os
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def setup_logging():
    log_directory = "test_logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_directory}/test_run_{timestamp}.log"
    
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

@pytest.fixture(params=["chrome"])  # İsterseniz "firefox", "edge" ekleyebilirsiniz
def driver(request):
    browser = request.param
    driver = None
    
    try:
        if browser == "chrome":
            options = ChromeOptions()
            # Test görünürlüğü için headless modu kapalı tutuyoruz
            driver = webdriver.Chrome(service=webdriver.ChromeService(ChromeDriverManager().install()), 
                                   options=options)
        elif browser == "firefox":
            options = FirefoxOptions()
            driver = webdriver.Firefox(service=webdriver.FirefoxService(GeckoDriverManager().install()),
                                    options=options)
        elif browser == "edge":
            options = EdgeOptions()
            driver = webdriver.Edge(service=webdriver.EdgeService(EdgeChromiumDriverManager().install()),
                                  options=options)
        
        if driver:
            driver.maximize_window()
            driver.implicitly_wait(10)
            logging.info(f"Starting test with {browser} browser")
            
    except Exception as e:
        logging.error(f"Failed to initialize {browser}: {str(e)}")
        raise
    
    yield driver
    
    if driver:
        driver.quit() 