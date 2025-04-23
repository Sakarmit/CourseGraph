def add_student_data(student):
    name = student["name"]
    arr = name.split(', ')
    with open("base_files/home.html", 'r') as file:
        data = file.read()
    moded_data = data.replace("[first-name]", arr[-1])
    with open("home.html", 'w+') as file:
        file.write(moded_data)

def update_graph_from_ex():
    with open("exTest.html", 'r') as file:
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
                <div class="filter">
                    <input id="filter" type="text" placeholder="Search...">
                </div>
                <div class="header-button">
                    <a href="faq.html">FAQ</a>
                </div>
                <div class="header-button">
                    <a href="#">Settings</a>
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