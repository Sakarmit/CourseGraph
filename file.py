import re
import degreeworks
def reset_profile_html():
    with open("profile_ref.html", "r", encoding="utf-8") as ref_file:
        ref_content = ref_file.read()

    # Write to the live profile file
    with open("profile.html", "w", encoding="utf-8") as profile_file:
        profile_file.write(ref_content)

    # Write to the base template copy
    with open("base_files/profile.html", "w", encoding="utf-8") as base_file:
        base_file.write(ref_content)

    print("profile.html and base_files/profile.html reset using profile_ref.html.")





def generate_class_and_class_grade(classes):
    html_rows = ""
    for course in classes:
        grade = course.get("letterGrade", "")
        credits = int(course.get("credits", 0))

        # Skip non-final grades and zero-credit entries
        if grade in ("*REG", "W", "QF") or credits == 0:
            continue

        course_name = f"{course['discipline']} {course['number']}"
        html_rows += (
            f"                    <tr>\n"
            f"                        <td class=\"question\">{course_name}</td>\n"
            f"                        <td class=\"question\">{grade}</td>\n"
            f"                    </tr>\n"
        )
    return html_rows


def update_profile_html_with_courses(course_list):
    with open("profile.html", "r", encoding="utf-8") as file:
        html = file.read()

    # This is the exact placeholder you want to detect
    original_block = '''            <div class="faq-item">
            <table>
                <tr>
                  <th class="question">Course</th>
                  <th class="question">Grade</th>
            </div>'''

    if original_block not in html:
        print("Skipping update: Course table has already been filled.")
        return

    # Generate course rows
    new_rows = generate_class_and_class_grade(course_list)

    # New full table block to insert
    new_block = f'''<div class="faq-item">
            <table>
                <tr>
                  <th class="question">Course</th>
                  <th class="question">Grade</th>
                </tr>
{new_rows}            </table>
        </div>'''

    # Perform replacement
    updated_html = html.replace(original_block, new_block)

    if degreeworks.noFetchMode == True:
        with open("base_files/profile.html", 'w+') as file:
            file.write(updated_html)
    with open("profile.html", 'w+') as file:
        file.write(updated_html)

    print("profile.html updated with course rows.")




def add_student_data(student):
    name = student["name"]
    arr = name.split(', ')
    with open("base_files/home.html", 'r') as file:
        data = file.read()
    moded_data = data.replace("[first-name]", arr[-1])
    with open("home.html", 'w+') as file:
        file.write(moded_data)


def add_profile_data(student):
    # Load the profile HTML template
    with open("profile.html", 'r') as file:
        data = file.read()
    
    # Split name to extract first name
    name_parts = student.get("name", "").split(", ")
    first_name = name_parts[-1] if len(name_parts) > 1 else student.get("name", "")
    
    # Replace placeholders with actual student data
    modded_data = data.replace("[first-name]", first_name)
    modded_data = modded_data.replace("[major]", student.get("major", "N/A"))
    modded_data = modded_data.replace("[gpa]", str(student.get("gpa", "N/A")))
    modded_data = modded_data.replace("[withdrawals-remaining]", str(student.get("withdrawals_left", "N/A")))
    modded_data = modded_data.replace("[credit_hours_applied]", str(student.get("total_credits", "N/A")))

    # Write the modified data to profile.html
    if degreeworks.noFetchMode == True:
        with open("base_files/profile.html", 'w+') as file:
            file.write(modded_data)
    with open("profile.html", 'w+') as file:
        file.write(modded_data)

def update_graph_from_ex():
    with open("ex.html", 'r') as file:
        data = file.read()
    #Remove unwanted tags
    data = data.replace("<h1></h1>", "")
    #Head tag
    moded_data = data.replace("<head>", """
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Graph Page</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@500&family=Konkhmer+Sleokchher&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="styling.css">              
            <script src="script.js"></script>
        """)
    #Body tag
    moded_data = moded_data.replace("<body>", """
        <body>
            <div class="header">
                <div>
                    <input class="filter" id="filter" type="text" placeholder="Search...">
                    <input class="checkbox" id="checkbox" type="checkbox">
                    <label for="checkbox" class="switch">Include Completed Courses</label>
                </div>
                <div>         
                    <div class="header-button">
                        <a href="faq.html">FAQ</a>
                    </div>
                    <div class="header-button">
                        <a href="profile.html">Profile</a>
                    </div>
                </div>
            </div>
        """)
    with open("ex.html", 'w+') as file:
        file.write(moded_data)

if __name__ == "__main__":
    student = {
        "name": "Doe, John",
    }
    add_student_data(student)
    update_graph_from_ex()
    print("Done")