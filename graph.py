from pyvis.network import Network
import networkx as nx

def make_graph():
    global graph
    graph=Network(notebook=True, directed=True)
    nxg = nx.Graph()
    graph.from_nx(nxg)

def add_node(_label):
    graph.add_node(graph.num_nodes() +1, label=_label)

    return graph.num_nodes()

def add_edge(_from, _to):
    graph.add_edge(_from, _to)

def draw_graph():
    graph.show("ex.html", notebook=False)
