import json
import requests
import os


def extract_prerequisites(prerequisites):
    ##an empty list to store formatted prerequisites
    formatted = []
    ##an empty list to store the current group of prerequisites
    current_group = []
    last_connector = None
    if not prerequisites:
        return "No prerequisites found"
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
num_courses = len(data["courseInformation"]["courses"])
for i in range(num_courses):
    course = data["courseInformation"]["courses"][i] 
    prerequisites = course["prerequisites"]
    print(extract_prerequisites(prerequisites))



classes = {
        "core_classes": [],
        "gen_eds": [],
        "conc_classes": [],  
        "all_possible_conc_classes": [],
        "all_classes": []
    }    
#Adds finished courses
def add_finished_courses(data, classes):
    if "fitList" in data and "classArray" in data["fitList"]:
        for classes_data in data["fitList"]["classArray"]:
            class_entry = {
                "discipline": classes_data.get("discipline"),
                "number": classes_data.get("number"),
                "credits": classes_data.get("credits"),
                "letterGrade": classes_data.get("letterGrade")
            }
            classes["all_classes"].append(class_entry)

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