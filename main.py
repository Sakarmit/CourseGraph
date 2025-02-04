from browser import create_browser_instance
from degreeworks import load_degree_works
import json
import os
browser = create_browser_instance()

try:
    with open('uncached/cookies.json', 'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            browser.add_cookie(cookie)
            cookie.domain = 'https://webauth.uncc.edu'
            browser.add_cookie(cookie)
except:
    print("No cookies to load")
browser.refresh()

load_degree_works(browser)
cookies = browser.get_cookies()
try:
    os.makedirs('uncached', exist_ok=True)
    file_path = 'uncached/cookies.json'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write('{}')
    with open(file_path, 'r') as file:
        json.dump(cookies, file)
except:
    print("Failed to save cookies")