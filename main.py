from browser import create_browser_instance
from degreeworks import load_degree_works
import graph

browser = create_browser_instance()

load_degree_works(browser)

graph.make_graph()
#Add nodes and edges here
# graph.draw_graph()