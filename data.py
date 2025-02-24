import json

def extract_prerequisites(prerequisites):
    ##an empty list to store formatted prerequisites
    formatted = []
    ##an empty list to store the current group of prerequisites
    current_group = []
    last_connector = None

    ##iterating through the prerequisites
    for prereq in prerequisites:
        ##extracting the course number and subject code
        course = f"{prereq['subjectCodePrerequisite']} {prereq['courseNumberPrerequisite']}"
        ##extracting the connector
        connector = prereq.get("connector", "")

        if last_connector and last_connector != connector:
            ##adding the current group to the formatted list
            formatted.append(f"({' or '.join(current_group)})" if last_connector == "O" else ' and '.join(current_group))
            current_group = []

        ##adding the course to the current group
        current_group.append(course)
        last_connector = connector

    ##adding the last group to the formatted list
    if current_group:
        formatted.append(f"({' or '.join(current_group)})" if last_connector == "O" else ' and '.join(current_group))

    ##joing the formatted list of prereq options with "and" connector
    return ' and '.join(formatted)

with open('req.json', 'r') as file:
    data = json.load(file)

##extracting the first course
course = data["courseInformation"]["courses"][0] 
prerequisites = course["prerequisites"]

print(extract_prerequisites(prerequisites))
