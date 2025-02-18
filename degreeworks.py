##importing seleniummodules for data scraping
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

##importing modules
import json
import os

degree_works = 'https://degreeworks.charlotte.edu/worksheets/WEB31'
user_id = None

"""
    load_degree_works function : Loads the Degree Works page and ensures the user is logged in.

    Args:
        browser: A selenium.webdriver instance used to interact with the
                 web page.
    """
def load_degree_works(browser):
    ## fetching degreeworks page
    browser.get(degree_works)
    if not 'https://degreeworks.charlotte.edu/worksheets/WEB31' == browser.current_url:
        log_in_user(browser)
    ## wait for page to load
    WebDriverWait(browser, 10)
    ## fetching degreeworks data
    get_degree_works_data(browser)

""" 
    log_in_user function : Logs in the user to the Degree Works page.

    Args:
        browser: A selenium.webdriver instance used to interact with the
                 web page.
"""
def log_in_user(browser):
    ## allow for user login
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

"""
    get_degree_works_data function : Fetches the data from the Degree Works page.

    Args:
        browser: A selenium.webdriver instance used to interact with the
                 web page.
    """
def get_degree_works_data(browser):
    ## finding user id
    user_id = browser.find_element(By.ID, "student-id").get_attribute("value")
    degreeDataFetch = f'''
    return fetch("https://degreeworks.charlotte.edu/api/audit?studentId={user_id}&school=UG&degree=BS&is-process-new=false&audit-type=AA&auditId=&include-inprogress=true&include-preregistered=true&aid-term=")
    .then(response => response.json())
    .then(data => data)
    .catch(error => error);
    '''

    result = browser.execute_script(degreeDataFetch)
    ## saving student data to json file 
    try:
        os.makedirs('uncached', exist_ok=True)
        file_path = 'uncached/file.json'
        with open(file_path, 'w+') as file:
            json.dump(result, file)
    ## messaging signaling error in saving json file
    except:
        print("Failed to save cookies")