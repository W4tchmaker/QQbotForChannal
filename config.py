import os

current_directory = os.path.dirname(os.path.abspath(__file__))

resources_name = "resources"
resources_path = os.path.join(current_directory, resources_name)
if not os.path.exists(resources_path):
    os.mkdir(resources_path)

SUPERUSERS = []
BLACK_LIST = []
WHITE_LIST = []
DEBUG = True
