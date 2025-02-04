from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import json
import os

degree_works = 'https://degreeworks.charlotte.edu/worksheets/WEB31'
user_id = None

def load_degree_works(browser):
    browser.get(degree_works)
    if not 'https://degreeworks.charlotte.edu/worksheets/WEB31' == browser.current_url:
        log_in_user(browser)
    WebDriverWait(browser, 10)
    get_degree_works_data(browser)

def log_in_user(browser):
    try:
        username_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_field = browser.find_element(By.ID, "password")
        login_button = browser.find_element(By.ID, "shibboleth-login-button")
    except:
        print("Failed to get username/password field")
        browser.quit()

    #Wait for Duo Verification
    try:
        WebDriverWait(browser, 600).until_not(
            EC.url_contains('https://api-c9cc3e0e.duosecurity.com/frame/v4/auth/prompt?sid=frameless-')
        )
        print("Successfully logged in")
    except:
        print("Failed to login")
        browser.quit()

    #Degree works
    try:
        WebDriverWait(browser, 600).until(
            EC.url_contains(degree_works)
        )
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "student-id"))
        )
    except:
        print("Failed to get Degreeworks after login")
        browser.quit()

def get_degree_works_data(browser):
    user_id = browser.find_element(By.ID, "student-id").get_attribute("value")
    testFetch = f'''
    return fetch("https://degreeworks.charlotte.edu/api/audit?studentId={user_id}&school=UG&degree=BS&is-process-new=false&audit-type=AA&auditId=&include-inprogress=true&include-preregistered=true&aid-term=")
    .then(response => response.json())
    .then(data => data)
    .catch(error => error);
    '''

    result = browser.execute_script(testFetch)
    try:
        os.makedirs('uncached', exist_ok=True)
        file_path = 'uncached/file.json'
        with open(file_path, 'w+') as file:
            json.dump(result, file)
    except:
        print("Failed to save cookies")