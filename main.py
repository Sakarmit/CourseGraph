import json
import os
from browser import create_browser_instance
from data import extract_all_classes, extract_prerequisites, get_unique_subjects, split_prereqs, split_requirements
from degreeworks import get_course_prereqs_range, get_degrees_data, load_degree_works
import graph

browser = create_browser_instance()

load_degree_works(browser)
# Open degreeworks and save user data to degreeworks.json if file does not exist
get_degrees_data(browser)

classes = {
    "requirements": [],
    "all_finished_classes": [],
    'insufficient': []
}

# Extract courses from degreeworks.json and store them in classes dictionary
extract_all_classes(classes)

# Extract unique range of subjects from classes dictionary
subject_range = get_unique_subjects(classes["all_finished_classes"])

# Retrieve all prerequisites for all courses in the subject range
subject_prereqs = []
for subject in subject_range:
    data = get_course_prereqs_range(browser, subject, subject_range[subject])["courseInformation"]["courses"]
    for course in data:
        subject_prereqs.append({
            "key": course["subjectCode"] + " " + course["courseNumber"],
            "subject": course["subjectCode"],
            "number": course["courseNumber"],
            "prerequisites": course["prerequisites"]
        })

graph.make_graph()

green = "#00b200"
red = "#b20000"
grey = "#808080"
light_grey = "#c0c0c0"

# Add all finished classes to the graph
for course in classes["all_finished_classes"]:    
    graph.add_node(course["key"], color=grey)

# Add incomplete requirements to the graph
for req in classes["requirements"]:
    if req.get("remaining_course_count", req.get("remaining_credit_count", 0)) == 0:
        continue

    courses = split_requirements(req.get("required", []))
    if len(courses) == 1:
        if len(courses[0]) == 1:
            graph.add_node_if_not_exists(courses[0][0], color=green)
            continue
        and_node = graph.add_node("AND", shape="circle", color=light_grey)
        for r in courses[0]:
            graph.add_node_with_edge(r, color=green, _to=and_node)
    else:
        or_node = graph.add_node("OR", shape="circle", color=light_grey)
        for subReqs in courses:
            if len(subReqs) == 1:
                string = subReqs[0]
                graph.add_node_with_edge(string, color=green, _to=or_node)
                continue

            and_node = graph.add_node("AND", shape="circle", color=light_grey)
            graph.add_edge(or_node, and_node)
            for r in subReqs:
                graph.add_node_with_edge(r, color=green, _to=and_node)

# Add all prerequisites to the graph
for course in classes["all_finished_classes"]:
    if "prerequisites" not in course:
        course["prerequisites"] = ""

        for prereq in subject_prereqs:
            if course["key"] == prereq["key"]:
                course["prerequisites"] = extract_prerequisites(prereq["prerequisites"])
                break

    if course["prerequisites"] == "":
        continue

    edges = split_prereqs(course["prerequisites"])
    for req in edges:
        if len(req) == 1:
            graph.add_node_with_edge(req[0], color=light_grey, _to=course["key"])
            continue
        
        for r in req:
            for completed in classes["all_finished_classes"]:
                if completed["key"] == r:
                    req = [r]
                    graph.add_edge(course["key"], req[0])
                    break
            
            if len(r) == 1:
                break
                

        if len(req) > 1:
            or_node = graph.add_node("OR", shape="circle", color=light_grey)
            graph.add_edge(course["key"], or_node)
            for r in req:
                graph.add_node_with_edge(r, color=light_grey, _to=or_node)

try:
    file_path = 'uncached/temp.json'
    print("SUCCESS")
    with open(file_path, 'w+') as file:
        json.dump(classes, file)
except:
    print("Failed to save AHHHHHH!!!")
    browser.quit()        

graph.draw_graph()

browser.get('file://' + os.path.realpath('home.html'))