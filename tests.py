import unittest
import graph
import data
from unittest.mock import patch, mock_open
import json
import data


#Unit testing for graph.py
class TestGraphFunctions(unittest.TestCase):

    def setUp(self):
        graph.nodes_dict.clear()
        graph.make_graph()

    def test_make_graph_creates_graph(self):
        self.assertIsNotNone(graph.graph)

    def test_add_node_creates_node(self):
        label = "Node1"
        node_id = graph.add_node(label)
        self.assertIn(node_id, graph.nodes_dict)
        self.assertTrue(graph.node_exists(node_id))

    def test_add_node_duplicate_label_adds_unique_id(self):
        graph.add_node("NodeA")
        node_id_2 = graph.add_node("NodeA")  
        self.assertNotEqual("NodeA", node_id_2)
        self.assertTrue(graph.node_exists("NodeA"))
        self.assertTrue(graph.node_exists(node_id_2))

    def test_add_edge_successful(self):
        n1 = graph.add_node("Start")
        n2 = graph.add_node("End")
        graph.add_edge(n1, n2)
        self.assertIn(n2, graph.nodes_dict[n1])

    def test_add_edge_prevents_duplicates(self):
        n1 = graph.add_node("Start")
        n2 = graph.add_node("End")
        graph.add_edge(n1, n2)
        graph.add_edge(n1, n2)
        self.assertEqual(graph.nodes_dict[n1].count(n2), 1)

    def test_add_edge_raises_error_for_missing_nodes(self):
        with self.assertRaises(Exception):
            graph.add_edge("NodeX", "NodeY")

    def test_node_exists_true(self):
        node_id = graph.add_node("CheckNode")
        self.assertTrue(graph.node_exists(node_id))

    def test_node_exists_false(self):
        self.assertFalse(graph.node_exists("FakeNode"))


class TestDataExtraction(unittest.TestCase):

    def test_courseString(self):
        course = {"discipline": "CS", "number": "1010"}
        self.assertEqual(data.courseString(course), "CS 1010")

    def test_courseArray_to_string_no_connector(self):
        courseArray = [{"discipline": "CS", "number": "1010"}, {"discipline": "MATH", "number": "1241"}]
        self.assertEqual(data.courseArray_to_string(courseArray), "CS 1010, MATH 1241")

    def test_courseArray_to_string_with_connector(self):
        courseArray = [{"discipline": "CS", "number": "1010"}, {"discipline": "MATH", "number": "1241"}]
        self.assertEqual(data.courseArray_to_string(courseArray, "or"), "CS 1010 or MATH 1241")

    def test_format_requirement(self):
        requirement = {
            "label": "Some Req",
            "percentComplete": "80%",
            "classesAppliedToRule": {"classArray": [{"discipline": "CS", "number": "1010"}]},
            "requirement": {
                "courseArray": [{"discipline": "MATH", "number": "1241"}],
                "creditsBegin": "6"
            },
            "creditsApplied": "3"
        }
        expected = {
            "label": "Some Req",
            "applied": "CS 1010",
            "percent_complete": "80%",
            "required": "MATH 1241",
            "remaining_credit_count": 3
        }
        self.assertEqual(data.format_requirement(requirement), expected)

    def test_get_unique_subjects(self):
        arr1 = ["CS 1010", "CS 1013", "CS 2010"]
        arr2 = ["MATH 1241"]
        expected = {"CS": [1010, 2010], "MATH": [1241, 1241]}
        self.assertEqual(data.get_unique_subjects(arr1, arr2), expected)

    def test_extract_prerequisites_and_or_logic(self):
        prereqs = [
            {"subjectCodePrerequisite": "CS", "courseNumberPrerequisite": "1010", "connector": "O"},
            {"subjectCodePrerequisite": "MATH", "courseNumberPrerequisite": "1241", "connector": "A"},
            {"subjectCodePrerequisite": "PHYS", "courseNumberPrerequisite": "1101", "connector": ""}
        ]
        result = data.extract_prerequisites(prereqs)
        self.assertEqual(result, "(CS 1010) and MATH 1241 and PHYS 1101")
    def test_extract_prerequisites_empty(self):
        self.assertEqual(data.extract_prerequisites([]), "")

    def test_split_prereqs(self):
        prereq_str = "(CS 1010 or MATH 1241) and PHYS 1101"
        expected = [["CS 1010", "MATH 1241"], ["PHYS 1101"]]
        self.assertEqual(data.split_prereqs(prereq_str), expected)

    def test_add_finished_courses(self):
        input_data = {
            "classInformation": {
                "classArray": [
                    {"discipline": "CS", "number": "1010", "credits": 3, "letterGrade": "A"},
                    {"discipline": "MATH", "number": "1241", "credits": 4, "letterGrade": "B"}
                ]
            }
        }
        classes = {"all_finished_classes": []}
        data.add_finished_courses(input_data, classes)
        self.assertEqual(len(classes["all_finished_classes"]), 2)
        self.assertEqual(classes["all_finished_classes"][0]["key"], "CS 1010")

    def test_add_insufficient_classes(self):
        input_data = {
            "insufficient": {
                "classArray": [
                    {"discipline": "CS", "number": "1010", "reasonInsufficient": "Low grade"}
                ]
            }
        }
        classes = {"insufficient": []}
        data.add_insufficient_classes(input_data, classes)
        self.assertEqual(classes["insufficient"][0]["reasonInsufficient"], "Low grade")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "classInformation": {"classArray": []},
        "blockArray": [],
        "insufficient": {"classArray": []}
    }))
    @patch("json.load")
    def test_extract_all_classes(self, mock_json_load, mock_file):
        mock_json_load.return_value = {
            "classInformation": {"classArray": []},
            "blockArray": [],
            "insufficient": {"classArray": []}
        }
        classes = {
            "all_finished_classes": [],
            "requirements": [],
            "insufficient": []
        }
        data.extract_all_classes(classes)
        self.assertIn("all_finished_classes", classes)
        self.assertEqual(len(classes["all_finished_classes"]), 0)

if __name__ == '__main__':
    unittest.main()