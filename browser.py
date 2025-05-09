import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_browser_instance():
    chrome_options = Options()

    uncached_folder = os.path.join(os.getcwd(), 'uncached', 'chrome-data')

    #chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    chrome_options.add_argument(f"--user-data-dir={uncached_folder}")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_experimental_option("detach", True)
    try:
        return webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Failed to create browser instance: {type(e)}")
        print(f"Common issues: Ensure previous browser instances are closed")
        exit()