import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
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

@pytest.fixture(params=["chrome"])
def browser(request):
    setup_logging()
    browser = None
    
    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--headless")  # Headless modu kapalı
        
        service = ChromeService()
        browser = webdriver.Chrome(service=service, options=options)
    
    browser.implicitly_wait(10)
    browser.maximize_window()
    logging.info(f"Starting {request.param} browser")
    
    yield browser
    
    logging.info(f"Closing {request.param} browser")
    browser.quit() 