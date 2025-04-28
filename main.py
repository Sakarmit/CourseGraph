import json
import os
import sys
from browser import create_browser_instance
from data import extract_all_classes, extract_prerequisites, get_unique_subjects, split_prereqs, split_requirements
from degreeworks import get_course_prereqs_ranges, get_degrees_data, load_degree_works
import degreeworks
from file import update_graph_from_ex
import graph

degreeworks.noFetchMode = "--noFetch" in sys.argv

green = "#00b200"
red = "#b20000"
grey = "#808080"
light_grey = "#c0c0c0"

classes = {
    "requirements": [],
    "all_finished_classes": [],
    'insufficient': [],
    'prerequisites': {},
}

# Courses for which prerequisites could have been retrieved but not added to the graph
unprocessed_classes = []
# Courses for which prerequisites have not been retrieved yet
backlog_classes = []

browser = create_browser_instance()

# Open degreeworks and save user data to degreeworks.json if file does not exist
load_degree_works(browser)
get_degrees_data(browser)
# Extract courses from degreeworks.json and store them in classes dictionary
extract_all_classes(classes, )

graph.make_graph()

finished_classes_keys = []
# Add all finished classes to the graph
for course in classes["all_finished_classes"]:
    if "ELE" in course["key"]:
        # Skip elective classes
        continue

    finished_classes_keys.append(course["key"])
    unprocessed_classes.append(course["key"])
    graph.add_node(course["key"], color=grey)

# Add incomplete requirements to the graph
for or_edges in classes["requirements"]:
    if or_edges.get("remaining_course_count", or_edges.get("remaining_credit_count", 0)) <= 0:
        continue

    courses = split_requirements(or_edges.get("required", []))
    if len(courses) == 1:
        if len(courses[0]) == 1:
            course = courses[0][0]
            if course not in unprocessed_classes:
                unprocessed_classes.append(course)
                graph.add_node(course, color=green)
                continue
        and_node = graph.add_node("AND", shape="circle", color=light_grey)
        for sub_or in courses[0]:
            if sub_or not in unprocessed_classes:
                unprocessed_classes.append(sub_or)
            graph.add_node_with_edge(sub_or, color=green, _from=and_node)
    else:
        or_node = graph.add_node("OR", shape="circle", color=light_grey)
        for subReqs in courses:
            if len(subReqs) == 1:
                string = subReqs[0]
                if string not in unprocessed_classes:
                    unprocessed_classes.append(string)
                graph.add_node_with_edge(string, color=green, _from=or_node)
                continue

            and_node = graph.add_node("AND", shape="circle", color=light_grey)
            graph.add_edge(or_node, and_node)
            for sub_or in subReqs:
                if sub_or not in unprocessed_classes:
                    unprocessed_classes.append(sub_or)
                graph.add_node_with_edge(sub_or, color=green, _from=and_node)

# Extract unique range of subjects from finished classes in classes dictionary
subject_prereqs = get_course_prereqs_ranges(browser, get_unique_subjects(unprocessed_classes))
# Add all courses prerequisites to the graph recursively
net_max = 0
while unprocessed_classes or backlog_classes:
    if not unprocessed_classes:
        unprocessed_classes = backlog_classes
        backlog_classes = []
        
        net_max += 1
        # Check if we have reached the maximum number of iterations
        # This is to prevent infinite loops in case of circular dependencies
        # or other issues with the prerequisites
        if net_max > 8:
            print("Failed to retrieve prerequisites for all courses")
            break
        for c in get_course_prereqs_ranges(browser, get_unique_subjects(unprocessed_classes)):
            for subject in subject_prereqs:
                if subject["key"] == c["key"]:
                     continue
            subject_prereqs.append(c)
            
    course = unprocessed_classes.pop()
    prereq = None
    for data in subject_prereqs:
        if course == data["key"]:
            prereq = extract_prerequisites(data["prerequisites"])
            break
    
    if prereq is None:
        backlog_classes.append(course)
        continue
    else:
        classes["prerequisites"][course] = prereq

    if len(prereq) == 0:
        continue

    and_edges = split_prereqs(prereq)
    for or_edges in and_edges:
        if len(or_edges) == 1:
            if graph.node_exists(or_edges[0]):
                graph.add_edge(course, or_edges[0])
                continue
            elif course in finished_classes_keys:
                # If the course is already finished, and has a uncompleted prerequisite, skip them
                continue
            
            unprocessed_classes.append(or_edges[0])
            graph.add_node_with_edge(or_edges[0], color=green, _from=course)
            continue
        
        for sub_or in or_edges:
            if sub_or in finished_classes_keys:
                # If the requirement is already fullfilled
                or_edges = [sub_or]
                graph.add_edge(course, or_edges[0])
                break
            
            if len(or_edges) == 1:
                break
                
        if len(or_edges) > 1:
            if course in finished_classes_keys:
                # If the course is already finished, and has a uncompleted prerequisite, skip them
                continue
            or_node = graph.add_node("OR", shape="circle", color=light_grey)
            graph.add_edge(course, or_node)
            for sub_or in or_edges:
                if graph.node_exists(sub_or):
                    graph.add_edge(or_node, sub_or)
                    continue

                unprocessed_classes.append(sub_or)
                graph.add_node_with_edge(sub_or, color=green, _from=or_node)      

graph.draw_graph()
update_graph_from_ex()
browser.get('file://' + os.path.realpath('home.html'))
sys.exit()