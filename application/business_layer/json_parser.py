import json
import os

class Parser:
    def __init__(self, json_file):
        file = open(os.path.abspath(json_file), 'r')
        self.json_data = json.load(file)

    def get_value(self, key):
        if key in self.json_data.keys():
            return self.json_data[key]
        else:
            return None