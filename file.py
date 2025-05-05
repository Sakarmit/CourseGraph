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
                        <a href="#">Profile</a>
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