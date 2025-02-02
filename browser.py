from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_browser_instance():
    chrome_options = Options()

    #chrome_options.add_argument("--headless=new")
    #chrome_options.add_argument("--auto-open-devtools-for-tabs")
    chrome_options.add_experimental_option("detach", True)
    
    return webdriver.Chrome(options=chrome_options)