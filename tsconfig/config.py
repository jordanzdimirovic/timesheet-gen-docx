import json
from json.decoder import JSONDecodeError
from os import path

DEFAULT_TSCONFIG_JSON_PATH = "config.json"

class TSConfig:
    __DATA: dict = None
    
    @staticmethod
    def load(json_path: str):
        # Ensure path is valid
        if not path.isfile(json_path):
            raise FileNotFoundError(f"Path '{json_path}' either doesn't exist")
        
        try:
            with open(json_path, "r") as f_conf:
                TSConfig.__DATA = json.loads(f_conf.read())
        
        except JSONDecodeError:
            raise ValueError(f"Configuration within '{json_path}' wasn't in valid JSON format")


    @staticmethod
    def get(key: str, default: callable = None) -> object:
        if type(key) is not str: raise ValueError(f"Key '{key}' was not a string")
        
        curr = TSConfig.__DATA
        key_spl = key.split(":")
        
        for part in key_spl:
            if type(curr) is not dict or part not in curr:
                if default: return default()
                else: raise KeyError(f"Configuration key not found: {key}")
            
            curr = curr[part]

        return curr
        