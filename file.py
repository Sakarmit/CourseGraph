def add_student_data(student):
    name = student["name"]
    arr = name.split(', ')
    with open("base_files/home.html", 'r') as file:
        data = file.read()
    moded_data = data.replace("[first-name]", arr[-1])
    with open("home.html", 'w+') as file:
        file.write(moded_data)
