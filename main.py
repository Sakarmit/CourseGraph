import json
import os
from browser import create_browser_instance
from data import extract_all_classes, extract_prerequisites, get_unique_subjects, split_prereqs
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

# Update all prerequisites for each finished course
for course in classes["all_finished_classes"]:
    if "prerequisites" in course:
        continue

    for prereq in subject_prereqs:
        if course["key"] == prereq["key"]:
            course["prerequisites"] = extract_prerequisites(prereq["prerequisites"])
            break
    
    if "prerequisites" not in course:
        course["prerequisites"] = ""

graph.make_graph()

green = "#00b200"
red = "#b20000"
grey = "#808080"
light_grey = "#c0c0c0"

# Add all finished classes to the graph
for course in classes["all_finished_classes"]:
    graph.add_node(course["key"])

# Add all prerequisites to the graph
for course in classes["all_finished_classes"]:
    if course["prerequisites"] == "":
        continue

    edges = split_prereqs(course["prerequisites"])
    for req in edges:
        if len(req) == 1:
            if not graph.node_exists(req[0]):
                graph.add_node(req[0])
            graph.add_edge(course["key"], req[0])
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
                if not graph.node_exists(r):
                    graph.add_node(r)
                graph.add_edge(or_node, r)

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