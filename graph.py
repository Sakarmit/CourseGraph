from pyvis.network import Network
import networkx as nx

nodes_dict = {}

def make_graph():
    global graph
    graph=Network(notebook=True, directed=True, select_menu=True)
    graph.barnes_hut(
        gravity=-2000, 
        central_gravity=0.1, 
        spring_length=100, 
        spring_strength=0.04
    )
    
    nxg = nx.Graph()
    graph.from_nx(nxg)
    graph.set_edge_smooth('dynamic')

def add_node(_label, shape="box", color="#204f37",title=""):   #check if node arrary exists, if not add to dict and add to node, else dont add to node. dictoinary.keys or something, get keys make sure it exists
    labelID = _label
    if isinstance(_label, str) and (_label in nodes_dict.keys()):
        labelID = _label + str(graph.num_nodes())
        
    if isinstance(labelID, str) and not (labelID in nodes_dict.keys()):
        nodes_dict[labelID] = []
    

    label_length = len(_label)
    width = max(50, 20 + label_length * 10)
    height = 50

    #node_id = graph.num_nodes() + 1
    graph.add_node(
    labelID,
    label=_label,
    shape=shape,
    color=color,
    width=width,
    height=height,
    font={'size': 20, 'color': 'white'},
    )

    return labelID

def add_edge(_from, _to, width=1, title="", arrows="to", dashes=False):  #if either node doesnt exist in dict, throw error node not found, if from node exists in dict add the to node to array 
    # if to node exists in the array of that from node DO NOT add that edge
    if isinstance(_from, str) and not (_from in nodes_dict.keys()):
        raise Exception(f"Node {_from} not found in nodes_dict. Please add node {_from} before adding edge {_from} -> {_to}")

    if isinstance(_to, str) and not (_to in nodes_dict.keys()):
        raise Exception(f"Node {_to} not found in nodes_dict. Please add node {_to} before adding edge {_from} -> {_to}")

    if _to in nodes_dict[_from]:
        return
    
    nodes_dict[_from].append(_to)
    
    graph.add_edge(
    _from,
    _to,
    width=width,
    title=title,
    arrows=arrows,
    dashes=dashes,
)
    
def node_exists(_label):
    return _label in nodes_dict.keys()

def add_edges_from_dict(edges_dict):
    for _from, to_list in edges_dict.items():
        from_id = nodes_dict.get(_from, _from)

        if not isinstance(to_list, list):
            to_list = [to_list]

        for to_item in to_list:
            if isinstance(to_item, (str, int)):
                to_id = nodes_dict.get(to_item, to_item)
                add_edge(from_id, to_id)

            elif isinstance(to_item, dict) and 'to' in to_item:
                to_id = nodes_dict.get(to_item['to'], to_item['to'])
                width = to_item.get('width', 1)
                title = to_item.get('title', "")
                arrows = to_item.get('arrows', "to")
                dashes = to_item.get('dashes', False)
                add_edge(from_id, to_id, width, title, arrows, dashes)

def draw_graph():
    graph.show("ex.html")
