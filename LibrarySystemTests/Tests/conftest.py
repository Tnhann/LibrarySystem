import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import logging
import os
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Logging yapılandırması
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

# Browser fixture'ları
@pytest.fixture
def driver():
    chrome_options = Options()
    driver = webdriver.Chrome(service=webdriver.ChromeService(ChromeDriverManager().install()), 
                            options=chrome_options)
    driver.implicitly_wait(10)
    setup_logging()
    logging.info("Starting test with Chrome browser")
    
    yield driver
    driver.quit() 