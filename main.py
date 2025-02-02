from browser import create_browser_instance
from degreeworks import load_degree_works
import json

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
with open('uncached/cookies.json', 'w') as file:
    json.dump(cookies, file)