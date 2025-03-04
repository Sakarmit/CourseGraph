##importing seleniummodules for data scraping
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

##importing modules
import json
import os

degree_works = 'https://degreeworks.charlotte.edu/worksheets/WEB31'

"""
    Loads the DegreeWorks page using the provided browser instance.

    This function navigates to the DegreeWorks page and ensures the user is logged in.
    It waits for the page to load and then fetches the DegreeWorks data.

    Args:
        browser: A browser instance used to interact with the webpage.
"""
def load_degree_works(browser):
    # Fetching degreeworks page
    browser.get(degree_works)
    if not 'https://degreeworks.charlotte.edu/worksheets/WEB31' == browser.current_url:
        log_in_user(browser)
    # Wait for page to load
    WebDriverWait(browser, 10)
    # Fetching degreeworks data
    get_degrees_data(browser)

""" 
    Logs in the user to the DegreeWorks page and ensure successful page load.

    Args:
        browser: A browser instance used to interact with the webpage.
"""
def log_in_user(browser):
    # Wait for User Login & Duo Verification
    try:
        WebDriverWait(browser, 600).until_not(
            EC.url_contains('https://api-c9cc3e0e.duosecurity.com/frame/v4/auth/prompt?sid=frameless-')
        )
        print("Successfully logged in")
    except:
        print("Failed to login")
        browser.quit()

    # Wait Degree works to load
    try:
        WebDriverWait(browser, 600).until(
            EC.url_contains(degree_works)
        )
        # Checking if page elements finished loading
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "student-id"))
        )
    except:
        print("Failed to get Degreeworks after login")
        browser.quit()

"""
    Fetches the user degrees data from the DegreeWorks page.

    Args:
        browser: A browser instance used to interact with the webpage.
"""
def get_degrees_data(browser):
    # Finding user id
    user_id = browser.find_element(By.ID, "student-id").get_attribute("value")
    # Finding user degree program
    user_program = browser.find_element(By.XPATH, "//span[text()='Program']/parent::div").text
    if "(UG)" in user_program:
        if "BS" in user_program:
            user_program = "UG&degree=BS"
        elif "BA" in user_program:
            user_program = "UG&degree=BA"
        else:
            print(f"Unsupported degree type - {user_program}")
            # browser.quit()
    elif "(GR)" in user_program:
        user_program = "GR&degree=MS" 
    else:
        print(f"Unsupported degree type - {user_program}")
        # browser.quit()

    # Fetch request which returns all user course data
    degreeDataFetch = f'''
    return fetch("https://degreeworks.charlotte.edu/api/audit?studentId={user_id}&school={user_program}&is-process-new=false&audit-type=AA&auditId=&include-inprogress=true&include-preregistered=true&aid-term=")
    .then(response => response.json())
    .then(data => data)
    .catch(error => error);
    '''

    result = browser.execute_script(degreeDataFetch)

    # Saving student data to json file 
    try:
        os.makedirs('uncached', exist_ok=True)
        file_path = 'uncached/file.json'
        with open(file_path, 'w+') as file:
            json.dump(result, file)
    except:
        print("Failed to save degree works data to file")
        browser.quit()

def get_course_prereqs(browser, subject, course_number):
    courseDataFetch = f'''
    return fetch("https://degreeworks.charlotte.edu/api/course-link?discipline={subject}&number={course_number}&")
    .then(response => response.json())
    .then(data => data)
    .catch(error => error);
    '''
    result = browser.execute_script(courseDataFetch)
    return result