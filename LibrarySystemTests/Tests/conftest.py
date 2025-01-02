import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import logging
import os
from datetime import datetime

def setup_logging():
    log_dir = "test_logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logging.basicConfig(
        filename=f"{log_dir}/test_{timestamp}.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

@pytest.fixture(params=["chrome"])  # Başlangıçta sadece Chrome ile test edelim
def browser(request):
    setup_logging()
    browser = None
    
    if request.param == "chrome":
        chrome_options = webdriver.ChromeOptions()
        service = ChromeService(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=chrome_options)
    
    browser.implicitly_wait(10)
    browser.maximize_window()
    logging.info(f"Starting {request.param} browser")
    
    yield browser
    
    logging.info(f"Closing {request.param} browser")
    browser.quit() 