import json

def extract_all_classes(classes, file_path='uncached/degreeworks.json'):
    with open(file_path) as file:
        data = json.load(file)
        add_finished_courses(data, classes)
        add_required_classes(data, classes)
        add_insufficient_classes(data, classes)

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

def courseString(course):
    return f"{course.get('discipline')} {course.get('number')}"

# List of courses that are not to be displayed
banned_courses = [" ", "@ @"]

def courseArray_to_string(courseArray, connector=None):
    simplified = []
    for course in courseArray:
        string_course = courseString(course)
        if string_course not in simplified and string_course not in banned_courses:
            simplified.append(string_course)
    return ", ".join(simplified) if connector == None else f" {connector} ".join(simplified)

def format_requirement(requirement):
    subRequirement = requirement.get("requirement", {})
    returnDict = {
        "label": requirement.get("label"),
        "applied": courseArray_to_string(requirement.get("classesAppliedToRule", {}).get("classArray", []), "and"),
        "percent_complete": requirement.get("percentComplete", "Unknown"),
        "required": courseArray_to_string(subRequirement.get("courseArray", []), "or")
    }
    if subRequirement.get("classesBegin") is not None:
        returnDict["remaining_course_count"] = int(subRequirement.get("classesBegin")) - int(requirement.get("classesApplied"))
    else:
        returnDict["remaining_credit_count"] = int(subRequirement.get("creditsBegin")) - int(requirement.get("creditsApplied"))

    return returnDict

# This function recursively evaluates the boolean evaluation of the requirement resulting in a list of requirements
def boolean_evaluation(requirement):
    resultRequirements = []
    req = requirement.get("requirement", {}).get("ifPart" if requirement.get("booleanEvaluation") == "True" else "elsePart", {}).get("ruleArray", [])
    for i in req:
        if i.get("booleanEvaluation") == None:
            if len(i.get("requirement", {}).get("courseArray", [])) == 0:
                continue
            resultRequirements.append(i)
        else:
            resultRequirements.extend(boolean_evaluation(i))

    return resultRequirements
def add_required_classes(data, classes):
    for item in data["blockArray"]:
        if item["requirementType"] in ["MAJOR", "CONC", "MINOR"]:
            for j in item['ruleArray']:
                if j.get("booleanEvaluation") == None:
                    if j.get("ruleArray") is not None:
                        for k in j["ruleArray"]:
                            classes["requirements"].append({**format_requirement(k), "master": item["requirementType"]})
                    elif j.get("classesAppliedToRule") is not None:
                        classes["requirements"].append({**format_requirement(j), "master": item["requirementType"]})
                else:
                    for k in boolean_evaluation(j):
                        if len(k.get("requirement", {}).get("courseArray", [])) == 0:
                            continue
                        classes["requirements"].append({**format_requirement(k), "master": item["requirementType"]})
        elif item.get("requirementValue") == "GENEDNEW" or item.get("requirementValue") == "GENED":
            for j in item['ruleArray']:
                if j.get("ruleArray") is not None:
                    for k in j.get("ruleArray"):
                        if k.get("booleanEvaluation") == None:
                            if k.get("classesAppliedToRule") == None:
                                applied = []
                                rules = []
                                for i in k.get("ruleArray"):
                                    rule = i.get("requirement", {}).get("courseArray", [])
                                    for apply in i.get("classesAppliedToRule", {}).get("classArray", []):
                                        applied.append(courseString(apply))
                                    if len(rule) < 2:
                                        continue
                                    
                                    courses = courseArray_to_string(rule, "and" if "With Lab" in k.get("label") else "or")
                                    if courses != "":
                                        rules.append(f'({courses})')
                                classes["requirements"].append({
                                    "label": k.get("label"),
                                    "applied": " and ".join(applied),
                                    "percent_complete": k.get("percentComplete", "Unknown"),
                                    "required": " or ".join(rules),
                                    "remaining_course_count": (2 if "With Lab" in k.get("label") else 1) - len(applied),
                                    "master": item["requirementValue"]
                                })
                            else:
                                classes["requirements"].append({**format_requirement(k), "master": item["requirementValue"]})
                        else:
                            for l in boolean_evaluation(k):
                                if len(l.get("requirement", {}).get("courseArray", [])) == 0:
                                    for m in l.get("ruleArray"):
                                        if m.get("percentComplete") == "Not Needed":
                                            continue
                                        classes["requirements"].append({**format_requirement(m), "master": item["requirementValue"]})
                                else:
                                    classes["requirements"].append({**format_requirement(l), "master": item["requirementValue"]})

def add_insufficient_classes(data, classes):
    if "insufficient" not in data or "classArray" not in data["insufficient"]:
        return
    for item in data["insufficient"].get('classArray'):
        insufficient = {
                "discipline": item.get("discipline"),
                "number": item.get("number"),
                "reasonInsufficient": item.get("reasonInsufficient"),

            }
        classes["insufficient"].append(insufficient)  # Add to list

# Extracts unique range of subjects from a multiple lists of classes
def get_unique_subjects(array):
    subject_ranges = {}
    for course in array:
        split = course.split(" ")
        if "ELE" in course[1]:
            continue
        discipline = split[0]
        # use only the first 4 characters of the course to get only the number
        number = int(split[1][:4])
        if discipline not in subject_ranges:
            subject_ranges[discipline] = [9999, 0000]

        if number < subject_ranges[discipline][0]:
            subject_ranges[discipline][0] = number
        if number > subject_ranges[discipline][1]:
            subject_ranges[discipline][1] = number + 1

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
    
    #joining the formatted list of prereq options with "and" connector
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

# Split the string of requirements into a list of requirements
def split_requirements(requirements):
    if not requirements:
        return []
    requirements = requirements.replace('(', "").replace(')', "")
    and_split_array = requirements.split(" or ")
    output = []
    for or_req in and_split_array:
        or_split_array = or_req.split(" and ")
        output.append(or_split_array)
    return output