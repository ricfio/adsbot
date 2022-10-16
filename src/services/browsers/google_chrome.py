"""Google Chrome"""
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class GoogleChrome(Chrome):
    """Google Chrome"""

    def __init__(self):
        chrome_driver = ChromeDriverManager().install()

        chrome_options = ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox') # required when running as root user
        chrome_options.add_argument('--display=host.docker.internal:0.0')
        chrome_options.add_argument('--disable-dev-shm-usage')

        super().__init__(service=Service(chrome_driver), options=chrome_options)
