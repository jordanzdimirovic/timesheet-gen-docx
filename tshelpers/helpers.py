import os
import re

import jsonpickle as jp

type regex = str | None

def iter_open(directory: str, match_fname: regex = None, fmode: str = 'r'):
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory '{directory}' not found")
    
    for base, _, files in os.walk(directory):
        for file in files:
            if not match_fname or re.search(match_fname, file):
                with open(os.path.join(base, file), "r") as f:
                    yield f


def iter_read(directory: str, match_fname: regex = None, transform: callable = None):
    for file in iter_open(directory, match_fname, 'r'):
        yield transform(file.read()) if transform else file.read()
