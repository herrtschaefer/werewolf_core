import importlib
import yaml


class config:
    def __init__(self, path=None):
        if path:
            with open(path, "r", encoding="utf-8") as conf_file:
                self.config = yaml.safe_load(conf_file)
        else:
            raise ValueError("path not provided")
    
    def isValid(self):
        