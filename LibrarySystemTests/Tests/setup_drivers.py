from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os

def setup_drivers():
    print("Setting up WebDrivers...")
    ChromeDriverManager().install()
    GeckoDriverManager().install()
    EdgeChromiumDriverManager().install()
    print("WebDrivers setup completed!")

if __name__ == "__main__":
    setup_drivers() 