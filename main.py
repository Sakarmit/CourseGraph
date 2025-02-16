from browser import create_browser_instance
from degreeworks import load_degree_works
import json
import os
browser = create_browser_instance()

load_degree_works(browser)