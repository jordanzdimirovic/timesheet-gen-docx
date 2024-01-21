from copy import deepcopy
from datetime import date
import os
import re
from types import NoneType

import jsonpickle as jp

import inspect

type regex = str | None

MONTH_NAMES = "January February March April May June July August September October November December".split(" ")

def pprint_date(d: date):
    return f"{MONTH_NAMES[d.month-1]} {d.day}, {d.year}"


def iter_open(directory: str, match_fname: regex = None, fmode: str = 'r'):
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory '{directory}' not found")
    
    for base, _, files in os.walk(directory):
        for file in files:
            if not match_fname or re.search(match_fname, file):
                with open(os.path.join(base, file), "r") as f:
                    yield f


def iter_read(directory: str, match_fname: regex = None, transform: callable = None, errors: list = None):
    for file in iter_open(directory, match_fname, 'r'):
        try:
            yield transform(file.read()) if transform else file.read()
        except UnicodeDecodeError as e:
            if errors: errors.append(file.name)
            else: print(f"Failed to decode file: '{file.name}'. Skipping...")


def dictify(obj: object):
    obj = deepcopy(obj)
    if not hasattr(obj, "__dict__"):
        # Non-dict type object
        if isinstance(curr, list):
            for i in range(len(curr)):
                curr[i] = dictify(curr[i])
                
            return curr
                
        elif not any(isinstance(curr[k], T) for T in (int, str, float, NoneType)):
            try:
                return str(curr)

            except:
                raise ValueError(f"Couldn't serialise field [{k} = {curr[k]}] (type: {type(curr[k])})")
        
        else:
            return curr
            
        
    curr = obj.__dict__
    
    props = {
        name: getattr(obj, name)
        for name, member in inspect.getmembers(type(obj)) if isinstance(member, property)
    }
    
    curr.update(props)

    for k in curr:
        if hasattr(curr[k], "__dict__"):
            curr[k] = dictify(curr[k])
            
        elif isinstance(curr[k], list):
            for i in range(len(curr[k])):
                curr[k][i] = dictify(curr[k][i])

        elif not any(isinstance(curr[k], T) for T in (int, str, float, NoneType)):
            try:
                curr[k] = str(curr[k])

            except:
                raise ValueError(f"Couldn't serialise field [{k} = {curr[k]}] (type: {type(curr[k])})")
    
    return curr