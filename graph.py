from pyvis.network import Network
import networkx as nx

def make_graph():
    global graph
    graph=Network(notebook=True, directed=True)
    graph.barnes_hut(
        gravity=-2000, 
        central_gravity=0.1, 
        spring_length=100, 
        spring_strength=0.04
    )
    
    nxg = nx.Graph()
    graph.from_nx(nxg)

def add_node(_label, shape="box", color="#204f37"):
    label_length = len(_label)
    width = max(50, 20 + label_length * 10)
    height = 50

    graph.add_node(
    graph.num_nodes() + 1,
    label=_label,
    shape=shape,
    color=color,
    width=width,
    height=height,
    font={'size': 20, 'color': 'white'},
)

    return graph.num_nodes()

def add_edge(_from, _to, width=1, title="", arrows="to", dashes=False):
    graph.add_edge(
    _from,
    _to,
    width=width,
    title=title,
    arrows=arrows,
    dashes=dashes,
)
    
def draw_graph():
    graph.show("ex.html", notebook=False)

if __name__ == "__main__":
    make_graph()

    graph.set_edge_smooth('dynamic')

    green = "#00b200"
    red = "#b20000"
    grey = "#808080"
    light_grey = "#c0c0c0"

    node1212 = add_node("ITSC 1212", color=grey)
    node1213 = add_node("ITSC 1213", color=grey)
    node2214 = add_node("ITSC 2214", color=green)
    node1600 = add_node("ITSC 1600", color=green)
    ornode = add_node("OR", shape="circle", color=light_grey)
    node2600 = add_node("ITSC 2600", color=green)
    node4155 = add_node("ITSC 4155", color=red)
    node3155 = add_node("ITSC 3155", color=red)
    node3300 = add_node("ITIS 3300", color=green)
    node3310 = add_node("ITIS 3310", color=green)
    ornode2 = add_node("OR", shape="circle", color=light_grey)

    add_edge(node1212, node1213)
    add_edge(node1213, node2214)
    add_edge(node1600, ornode)
    add_edge(node2600, ornode)
    add_edge(node2214, node4155)
    add_edge(node3155, ornode2)
    add_edge(node3300, ornode2)
    add_edge(node3310, ornode2)
    add_edge(ornode2, node4155)
    add_edge(node2214, node3155)
    
    draw_graph()