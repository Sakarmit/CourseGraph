import json

def extract_all_classes(classes, file_path='uncached/degreeworks.json'):
    with open(file_path) as file:
        data = json.load(file)
        add_finished_courses(data, classes)
        add_core_classes(data, classes)
        add_concentration_classes(data, classes)

#Adds finished courses
def add_finished_courses(data, classes):
    if not ("classInformation" in data and "classArray" in data["classInformation"]):
        print("No class information in data")
        return
    
    for classes_data in data["classInformation"]["classArray"]:
        class_entry = {
            "key": classes_data.get("discipline") + " " + classes_data.get("number"),
            "discipline": classes_data.get("discipline"),
            "number": classes_data.get("number"),
            "credits": classes_data.get("credits"),
            "letterGrade": classes_data.get("letterGrade")
        }
        classes["all_finished_classes"].append(class_entry)

#Adds finished core classes
def add_core_classes(data, classes):
    for item in data["blockArray"]:
        if item["requirementType"] == "MAJOR":
            for j in item['ruleArray']:
                if j.get("labelTag") == "CORE":
                    for k in j["ruleArray"]:
                        class_entry = {
                            "label": k.get("label"),
                            "discipline": k.get('classesAppliedToRule', {}).get('classArray', [{}])[0].get("discipline", "Unknown"),
                            "percent_complete": item.get("percentComplete", "Unknown"),
                            "number": k.get('classesAppliedToRule', {}).get('classArray', [{}])[0].get("number", "Unknown"),
                            "credits": k.get("creditsApplied"),
                            "letterGrade": k.get('classesAppliedToRule', {}).get('classArray', [{}])[0].get("letterGrade", "Unknown"),
                            "OR": [
                                {"discipline": alt.get("discipline", "Unknown Alternative"),
                                 "number": alt.get("number", "Unknown number")}
                                for alt in k.get("requirement", {}).get("courseArray", [])
                            ]
                        }
                        classes["core_classes"].append(class_entry)

#Adds concentration course selection
def add_concentration_classes(data, classes):
    for item in data["blockArray"]:
        if item["requirementType"] == "CONC":
            for k in item['ruleArray']:
                if "requirement" in k:
                    for x in k.get("requirement", {}).get("courseArray", []):
                        class_entry = {
                            "discipline": x.get("discipline"),
                            "number": x.get("number")
                        }
                        classes["all_possible_conc_classes"].append(class_entry)

# Extracts unique range of subjects from a multiple lists of classes
def get_unique_subjects(*arrays):
    subject_ranges = {}
    for array in arrays:
        for course in array:
            if "ELE" in course["number"]:
                continue
            discipline = course["discipline"]
            # use only the first 4 characters of the course to get only the number
            number = int(course["number"][:4])
            if discipline not in subject_ranges:
                subject_ranges[discipline] = [9999, 0000]

            if number < subject_ranges[discipline][0]:
                subject_ranges[discipline][0] = number
            if number > subject_ranges[discipline][1]:
                subject_ranges[discipline][1] = number

    return subject_ranges

def extract_prerequisites(prerequisites):
    #an empty list to store formatted prerequisites
    formatted = []
    #an empty list to store the current group of prerequisites
    current_group = []
    last_connector = None
    if not prerequisites:
        return ""
    #iterating through the prerequisites
    for prereq in prerequisites:
        if prereq['subjectCodePrerequisite'] == "":
            continue

        #extracting the course number and subject code
        course = f"{prereq['subjectCodePrerequisite']} {prereq['courseNumberPrerequisite']}"
        #extracting the connector
        connector = prereq.get("connector", "")

        if last_connector != None and last_connector != connector and connector == "A":
            #adding the current group to the formatted list
            formatted.append(f"({' or '.join(current_group)})" if last_connector == "O" else ' and '.join(current_group))
            current_group = []

        #adding the course to the current group
        current_group.append(course)
        last_connector = connector

    if len(formatted) == 0:
        formatted.append(f"{' or '.join(current_group)}" if last_connector == "O" else ' and '.join(current_group))
    else:
        formatted.append(f"({' or '.join(current_group)})" if last_connector == "O" else ' and '.join(current_group))
    
    #joing the formatted list of prereq options with "and" connector
    return ' and '.join(formatted)

# Splits the string of prerequisites into a array of arrays format
def split_prereqs(prereqs):
    if not prereqs:
        return []
    prereqs = prereqs.replace('(', "").replace(')', "")
    and_split_array = prereqs.split(" and ")
    output = []
    for or_req in and_split_array:
        or_split_array = or_req.split(" or ")
        output.append(or_split_array)
    return output