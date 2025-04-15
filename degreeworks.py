#importing seleniummodules for data scraping
from file import add_student_data
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#importing modules
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

def get_user_info(browser):
    userInfoFetch = '''
        return fetch("https://degreeworks.charlotte.edu/api/students/myself")
        .then(response => response.json())
        .then(data => data)
        .catch(error => error);
    '''
    result = browser.execute_script(userInfoFetch)
    try:
        student = {}
        
        subpart = result['_embedded']['students'][0]
        student['id'] = subpart['id']
        student['name'] = subpart['name']

        goal0 = subpart['goals'][0]

        student['program_level'] = goal0['school']['key']
        student['program_type'] = goal0['degree']['key']

        return student
    except:
        print("Failed to get user info")
        browser.quit()
"""
    Fetches the user degrees data from the DegreeWorks page.

    Args:
        browser: A browser instance used to interact with the webpage.
"""
def get_degrees_data(browser):
    student = get_user_info(browser)
    # Fetch request which returns all user course data
    degreeDataFetch = f'''
    return fetch("https://degreeworks.charlotte.edu/api/audit?studentId={student['id']}&school={student['program_level']}&degree={student['program_type']}&is-process-new=false&audit-type=AA&auditId=&include-inprogress=true&include-preregistered=true&aid-term=")
    .then(response => response.json())
    .then(data => data)
    .catch(error => error);
    '''

    result = browser.execute_script(degreeDataFetch)

    # Add extra data to student object
    student['gpa'] = result['auditHeader']['studentSystemGpa']
    
    add_withdrawal_failures_to_student(student, result)

    add_student_data(student)
    # Saving student degree data to json file 
    try:
        os.makedirs('uncached', exist_ok=True)
        file_path = 'uncached/student.json'
        with open(file_path, 'w+') as file:
            json.dump(student, file)
    except:
        print("Failed to save student data to file")
        browser.quit()

    # Saving student degree data to json file 
    try:
        os.makedirs('uncached', exist_ok=True)
        file_path = 'uncached/degreeworks.json'
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

# Fetches the prerequisites for a range of courses in a subject
def get_course_prereqs_range(browser, subject, range):
    courseDataFetch = f'''
    return fetch("https://degreeworks.charlotte.edu/api/course-link?discipline={subject}&number={range[0]}%3A{range[1]+1}&=")
    .then(response => response.json())
    .then(data => data)
    .catch(error => error);
    '''
    result = browser.execute_script(courseDataFetch)
    return result

def add_withdrawal_failures_to_student(student, audit_data):
    # Get the classArray from 'insufficient' section
    classes = audit_data.get("insufficient", {}).get("classArray", [])

    # Fallback: if classArray isn't there, use the root-level classArray
    if not classes:
        classes = audit_data.get("classArray", [])

    # Count grades
    num_withdrawals = sum(1 for c in classes if c.get("letterGrade") == "W")
    num_qf = sum(1 for c in classes if c.get("letterGrade") == "QF")

    # Add to student dict
    student["withdrawals"] = num_withdrawals
    student["failures"] = num_qf
