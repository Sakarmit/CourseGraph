import unittest
import graph

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

if __name__ == '__main__':
    unittest.main()